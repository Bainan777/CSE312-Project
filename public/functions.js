let socket = io();

function upvote(postID) {
    socket.emit('upvote', postID);
}

function downvote(postID) {
    socket.emit('downvote', postID);
}

function loadToggle() {
    socket.emit('load_toggle')
    /**
     * TODO: add functionality to update colors of buttons accordingly. check mongo compass to make sure variable accesses are correct. may have to emit -> server.py -> emit back here
     */
}

socket.on('vote_update', function(data) {
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