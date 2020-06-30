let ms = 0
let s = 0
let m = 0
let timer
let isPaused = true


let stopwatchEl = document.querySelector('.stopwatch')
let startButton = document.querySelector('#start')
let pauseButton = document.querySelector('#pause')
let stopButton = document.querySelector('#stop')
let resetButton = document.querySelector('#reset')
let resumeButton = document.querySelector('#resume')
let result = stopwatchEl.textContent


function startTime() {
    if(!timer) {
        timer = setInterval(run, 10)
        $(startButton).hide()
        $(pauseButton).show()
        $(stopButton).hide()
    }
}

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

function pauseTime() {
    result = stopwatchEl.textContent
    $(pauseButton).hide()
    $(stopButton).show()
    $(startButton).show()
    stop()
}


function stopTimer() {
    result = stopwatchEl.textContent
    stop()
    ms = 0
    s = 0
    m = 0
    stopwatchEl.textContent = getTimer()
    $(stopButton).hide()
    $(startButton).show()
}


function stop() {
    clearInterval(timer)
    timer = false
}

function resetTimer() {
    stopTimer()
    startTime()
}


function getTimer() {
    return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s) + ':' + (ms < 10 ? '0' + ms : ms)
}

