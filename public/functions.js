var socket = io.connect('/');

function upvote(postID) {
    socket.emit('upvote', postID);
    console.log('\n----------FUNCTIONS.JS UPVOTE----------\n')
}

function downvote(postID) {
    socket.emit('downvote', postID);
    console.log('\n----------FUNCTIONS.JS DOWNVOTE----------\n')
}

function loadToggle() {
    socket.emit('load_toggle')
    /**
     * TODO: add functionality to update colors of buttons accordingly. check mongo compass to make sure variable accesses are correct. may have to emit -> server.py -> emit back here
     */
}

socket.on('vote_update', function(data) {
    console.log('\n----------FUNCTIONS.JS VOTE_UPDATE----------\n')
    let postID = data.post_id;
    let votes = document.getElementById(`vote-count-${postID}`);
    votes.textContent = data.votes;

    let icon; 

    let upvote_icon = document.getElementById(`upvote-${postID}`)
    let downvote_icon = document.getElementById(`downvote-${postID}`)

    if (data.upvoted) {
        icon = upvote_icon;
        // if upvote is clicked but downvote was clicked, toggle downvote styling off
        if (downvote_icon.classList.contains('icon-clicked')) {
            downvote_icon.classList.toggle('icon-clicked');
        }
    } else if (data.downvoted) {
        icon = downvote_icon;
        // if downvote is clicked but upvote was clicked, toggle upvote styling off
        if (upvote_icon.classList.contains('icon-clicked')) {
            upvote_icon.classList.toggle('icon-clicked');
        }
    }

    icon.classList.toggle('icon-clicked');
})
 
// To access the stars

// Star Code from: https://www.geeksforgeeks.org/star-rating-using-html-css-and-javascript/ 
// Funtion to update rating
function gfg(n) {
    remove();
    let stars = document.getElementsByClassName("star-rating");
    let output = document.getElementById("output-rating");
    for (let i = 0; i < n; i++) {
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        stars[i].className = "star-rating " + cls;
    }
    output.value = n + "/5";
}
 
// To remove the pre-applied styling
function remove() {
    let i = 0;
    let stars = document.getElementsByClassName("star-rating");
    while (i < 5) {
        stars[i].className = "star-rating";
        i++;
    }
}

socket.on('post:scheduled', (data) => {
    console.log("received 'post:scheduled' event", data);
    const scheduledAt = new Date(data.scheduledAt);
    let postID = data.id;
    function clearInterval(){
        let countdownDiv = document.createElement('div');
            countdownDiv.id = 'sch-countdown-' + postID;

            let wrapper = document.querySelector('.sch-post-wrapper');
            wrapper.appendChild(countdownDiv);
            document.getElementById('sch-countdown-' + postID).innerHTML = `
            <span>0</span> days 
            <span>0</span> hours
            <span>0</span> minutes
            <span>0</span> seconds`
    }
    const countdownInterval = setInterval(() => {
        const now = new Date();
        const remainingTime = scheduledAt - now;

        if (remainingTime <= 0) {
            clearInterval(countdownInterval);
        } else {
            let days = Math.floor(remainingTime / 86400000);
            let hours = Math.floor(remainingTime % 3600000);
            let minutes = Math.floor(remainingTime % 60000); 
            let seconds = Math.floor(remainingTime % 1000);

            let countdownDiv = document.createElement('div');
            countdownDiv.id = 'sch-countdown-' + postID;

            let wrapper = document.querySelector('.sch-post-wrapper');
            wrapper.appendChild(countdownDiv);
            document.getElementById('sch-countdown-' + postID).innerHTML = `
            <span>${days}</span> days 
            <span>${hours}</span> hours
            <span>${minutes}</span> minutes
            <span>${seconds}</span> seconds`;
        console.log(`Time remaining: ${hours}h ${minutes}m ${seconds}s`);
        }
    }, 1000); // Update every second
    });