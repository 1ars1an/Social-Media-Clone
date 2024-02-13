document.addEventListener('DOMContentLoaded', () => {
    load_content();

    document.querySelectorAll('.editor').forEach(e_btn => {
        e_btn.addEventListener('click', () => {
            var p_id = e_btn.dataset.postId;
            load_form(p_id);
        });
    })

    document.querySelectorAll('.hider').forEach(e_btn => {
        e_btn.addEventListener('click', () => {
            var d_id = e_btn.dataset.destroyId;
            console.log(d_id);
            hide_post(d_id);
        });
    })

    document.querySelectorAll('.liker').forEach(e_btn => {
        e_btn.addEventListener('click', () => {
            var p_id = e_btn.dataset.lpostah;
            like_handler(p_id);
        });
    })
})

function like_handler(p_id) {
    p_id = p_id.toString();
    const likedpost = 'lepostah-' + p_id;

    //get list of liked posts
    fetch('/likedapi')
    .then(response => response.json())
    .then(result => {
        likeList = result['likeList'];
        //check if post is liked or not
        if (likeList.indexOf(Number(p_id)) >= 0) {
            var liked = true;
        }
        else {
            var liked = false
        }

        if (liked === true) {
            fetch(`/unlike/${p_id}`)
            .then(response => response.json())
            .then(message => {
                document.querySelector(`#${likedpost}`).innerHTML = 'Like!';

            })
        }
        else {
            fetch(`/like/${p_id}`)
            .then(response => response.json())
            .then(message => {
                document.querySelector(`#${likedpost}`).innerHTML = 'Unlike!';
            })
        }
    })
}

function load_content() {
    document.querySelectorAll('.to-hide').forEach(div => {
        div.style.display = 'block';
    })
    document.querySelectorAll('.to-show').forEach(div => {
        div.style.display = 'none';
    })
};

function load_form(p_id) {
    const cnt_div = 'hide-' + p_id.toString();
    const frm_div = 'show-' + p_id.toString();
    
    document.querySelector(`#${cnt_div}`).style.display = 'none';
    document.querySelector(`#${frm_div}`).style.display = 'block';
};

function hide_post(d_id) {
    const wrapper = document.createElement('div');
    wrapper.className = 'mx-auto text-center m-5';

    const reverse = document.createElement('button');
    reverse.textContent = 'Undo';
    reverse.className = 'btn btn-success';
    reverse.id = 'undo-' + d_id.toString();
    reverse.addEventListener('click', () => {
        unhide_post(d_id, reverse.id);
    })
    wrapper.appendChild(reverse);

    const to_hide = 'post-' + d_id.toString()
    curr_post = document.querySelector(`#${to_hide}`)
    curr_post.after(wrapper);
    curr_post.style.display = 'none';
}

function unhide_post(d_id, uh_id) {
    const to_show = '#post-' + d_id.toString() 
    document.querySelector(`#${uh_id}`).remove();
    document.querySelector(`${to_show}`).style.display = 'block';
}