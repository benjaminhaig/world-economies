/*

Script used for typewriter effect
Will work for all elements with the ID "typewriter"

*/


let letterCount = 0
const letterTiming = 200
const title = document.getElementById("typewriter")
const originalText = title.textContent

title.textContent = "_";

const updateText = () => {
    const title = document.getElementById("typewriter")
    title.textContent = originalText.slice(0, letterCount) + "_"

    if (letterCount > originalText.length) {
        clearInterval(interval)
        title.textContent = originalText
    }
}

interval = setInterval(() => {
    letterCount++
    updateText()
}, letterTiming)


