document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.editpost').forEach(post => {
        post.onclick = function() {
            edit_post(this.dataset.postid);
        }
    });

    document.querySelectorAll('.like').forEach(post => {
        post.addEventListener('click', () => like_post(post.dataset.postid));
    });


    document.querySelectorAll('.unlike').forEach(post => {
        post.addEventListener('click', () => unlike_post(post.dataset.postid));
    });

});

function edit_post(post) {

    const element = document.createElement('div');
    element.setAttribute('id', 'element');
    element.setAttribute('class', 'container post-element');
    
    let textbox = document.createElement('textarea');
    textbox.setAttribute('id', 'textbox');
    textbox.setAttribute('class', 'form-control');
    textbox.innerHTML = document.getElementById(`post_text-${post}`).innerHTML;

    const button = document.createElement('button');
    button.setAttribute('id','save');
    button.setAttribute('class', 'btn btn-success');
    button.innerHTML = "Save";

    document.getElementById(`${post}-body`).style.display = 'none';

    document.getElementById(`${post}-container`).append(element);
    document.getElementById('element').appendChild(textbox);
    document.getElementById('element').appendChild(button);

    document.getElementById('save').addEventListener('click', () => submit_edit_post(post));
}

function submit_edit_post(post) {

    const text = document.querySelector('#textbox').value;
    save_post(post, text);
    return false;

}

function save_post(id, text) {

    fetch('/save', {
        method: 'POST', 
        body: JSON.stringify({
        id: id,
        text: text
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
    
    document.getElementById(`${id}-body`).style.display = 'block';
    edit_window = document.getElementById('element');
    edit_window.remove();

    document.getElementById(`post_text-${id}`).innerHTML = text;
    
}


function like_post(postid) {

    fetch("/like", {
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({
            post: postid
        })
    })
    .then(response => response.json())
    .then(result => {
        if(result['message'] === "success") {
            document.querySelector(`#heart-${postid}`).src = "/static/network/redheart.png"
            let likes = parseInt(document.querySelector(`#likes-${postid}`).innerHTML);
            likes++;
            if(likes === 1) {
                document.querySelector(`#likes-${postid}`).innerHTML = likes + " Like";
            }
            else {
                document.querySelector(`#likes-${postid}`).innerHTML = likes + " Likes";
            }
            document.querySelectorAll('.like').forEach(post => {
                if (post.dataset.postid === postid) {
                    classes = post.className.replace('like', 'unlike');
                    post.className = classes;
                    post.removeEventListener('click', () => like_post(post.dataset.postid));
                    post.addEventListener('click', () => unlike_post(post.dataset.postid));
                }
            });
        }
        else {
            p = document.createElement('p');
            p.innerHTML = result['message'];
            document.querySelector(`#like-${postid}`).appendChild(p);
        }
    })
}

function unlike_post(postid) {

    fetch("/unlike", {
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({
            post: postid
        })
    })
    .then(response => response.json())
    .then(result => {
        if(result['message'] === "success") {
            document.querySelector(`#heart-${postid}`).src = "/static/network/heart.png"
            let likes = parseInt(document.querySelector(`#likes-${postid}`).innerHTML);
            likes--;
            if(likes === 1) {
                document.querySelector(`#likes-${postid}`).innerHTML = likes + " Like";
            }
            else {
                document.querySelector(`#likes-${postid}`).innerHTML = likes + " Likes";
            }
            document.querySelectorAll('.unlike').forEach(post => {
                if (post.dataset.postid === postid) {
                    classes = post.className.replace('unlike', 'like');
                    post.className = classes;
                    post.removeEventListener('click', () => unlike_post(post.dataset.postid));
                    post.addEventListener('click', () => like_post(post.dataset.postid));
                }
            });
        }
        else {
            p = document.createElement('p');
            p.innerHTML = result['message'];
            document.querySelector(`#like-${postid}`).appendChild(p);
        }
    })
}
