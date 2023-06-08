if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
    }

function playSelectAudio() {
    let audio = document.getElementById("selectsound");
    audio.play()
}

function playLoseAudio() {
    let audio = document.getElementById("losesound");
    audio.play()
}

function playWinAudio() {
    let audio = document.getElementById("winsound");
    audio.play()
}

function playWinAudioHard() {
    let audio = document.getElementById("winsoundhard");
    audio.play()
}

function playGameAudioOne() {
    let audio = document.getElementById("gameaudio")
    audio.play()
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function buttonColor(id) {
    let correct = document.getElementById(id).getAttribute("value");
    let audio = document.getElementById("gameaudio");
    let stage = document.getElementById("stage").getAttribute("value");
    $(audio).animate({volume: 0}, 800);

    document.getElementById(id).style.backgroundColor = '#ff9900';
    $(':button').prop('disabled', true);
    $(":button").css("opacity", "50%");
    document.getElementById(id).style.opacity = '100%';

    setTimeout(function() {
        if (correct == 0) {
            document.getElementById(id).style.backgroundColor = '#ff4d4d';
            playLoseAudio();
        }
        else {
            document.getElementById(id).style.backgroundColor = '#03fc4e';
            if (stage < 5) {
                playWinAudio();
            }
            else {
                playWinAudioHard();
            }
            setTimeout(function() {
                $('#exampleModal').modal('show')
                }, 1500);
        }
        }, 2800);
}
