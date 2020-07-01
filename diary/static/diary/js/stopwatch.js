var ms = 0
var s = 0
var m = 0
var timer
var isPaused = true


var stopwatchEl = document.querySelector('.stopwatch')
var startButton = document.querySelector('#start')
var pauseButton = document.querySelector('#pause')
var stopButton = document.querySelector('#stop')
var resetButton = document.querySelector('#reset')
var resumeButton = document.querySelector('#resume')
var result = stopwatchEl.textContent


$(document).on('click', '#start', function() {
    if(!timer) {
        timer = setInterval(run, 10)
        $(startButton).hide()
        $(pauseButton).show()
        $(stopButton).hide()
    }
})


function run () {
    stopwatchEl.textContent = getTimer()
    ms++
    if(ms == 100) {
        ms = 0
        s++
    }
    if(s == 60) {
        s = 0
        m++
    }
}

$('#pause').on('click', function() {
    result = stopwatchEl.textContent
    $(pauseButton).hide()
    $(stopButton).show()
    $(startButton).show()
    stop()
})


$('#stop').on('click', function() {
    result = stopwatchEl.textContent
    stop()
    ms = 0
    s = 0
    m = 0
    stopwatchEl.textContent = getTimer()
    $(stopButton).hide()
    $(startButton).show()
})


function stop() {
    clearInterval(timer)
    timer = false
}

$('#reset').on('click', function() {
    stopTimer()
    startTime()
})


function getTimer() {
    return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s) + ':' + (ms < 10 ? '0' + ms : ms)
}

