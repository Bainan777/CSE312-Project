function welcome(){
    alert("This is a placeholder Javascript function! Expect more in the coming future.");
    setTimeout(3000);
}

// upvote toggle button functionality

function toggleUpvote(postId, buttonElement){
    const isUpvoted = buttonElement.classList.contains('upvoted');
    const url = isUpvoted ? `/un-upvote/${postId}` : `/upvote/${postId}`;
    const icon = buttonElement.querySelector('i');

    fetch(url, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                buttonElement.classList.toggle('upvoted');
                buttonElement.classList.toggle('not-upvoted');
                icon.classList.toggle('fa-solid');
                icon.classList.toggle('fa-regular');
                const upvoteCount = document.getElementById(`upvote-count-${postId}`);
                upvoteCount.textContent = data.upvoteCount;
            } 
        })
}