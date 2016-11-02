var webdriver = require('selenium-webdriver'),
    By = webdriver.By
    promise = webdriver.promise;

var driver = new webdriver.Builder()
    .forBrowser('chrome')
    .build();

var times = [];

console.log('Current datetime: ' + new Date());
console.log('\nMovie type: IMAX-3D\n');

driver.get('http://planetakino.ua/showtimes/#imax-3d');
driver.getTitle().then(function(title) {
    console.log('Opened page: ' + title + '\n');
});

driver.findElements(By.css('.showtime-movie-container :not(.hidden).movie-title'))
    .then(function(elements) {
        console.log('Found ' + elements.length + ' movie(s):')
        elements.forEach(function(element) {
            element.getText().then(function(text) {
                console.log(text);
            })
        });
    });

driver.findElement(By.css(':not(.hidden).p-one-day'))
    .then(function(element) {
        element.findElement(By.css('.dates')).getText().then(function(text) {
            console.log('\nTop date is: ' + text);
        })
        return element;
    })
    .then(function(element) {
        element.findElements(By.css('.t-imax-3d .time:not(.past)')).then(function(timeElements) {
            console.log('Found ' + timeElements.length + ' upcoming sessions:');
            timeElements.forEach(function(timeElement) {
                timeElement.getText().then(function(text) {
                    times.push(text.trim());
                    console.log(text);
                })
            })
        })
        console.log();
        return element;
    })
    .then(function(element) {
        times.forEach(function(time) {
            element.findElement(By.xpath("//a[contains(text(), '" + time + "')]")).then(function(e) {
                e.click();
                console.log('Opened session for: ' + time);
                driver.findElements(By.css('.hs-image-0000000001')).then(function(seatElements) {
                    seatElements.forEach(function(seatElement) {
                        var seatInfo = "";
                        seatElement.getAttribute('exp-data-row').then(function(attribute) {
                            seatInfo += 'Row: ' + attribute;
                        })
                        seatElement.getAttribute('exp-data-col').then(function(attribute) {
                            seatInfo += 'Col: ' + attribute;
                        })
                        console.log(seatInfo);
                    })
                })
            })
        })
    });
