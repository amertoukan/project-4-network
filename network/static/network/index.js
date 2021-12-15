/**
 * Edit Post
 */

edit_post = (post_id) => {
    //Find content 
    let post_div = document.getElementById(`post_div_${post_id}`)
    let area = post_div.children[0]; 
    const content = area.innerHTML
    //remove content
    area.remove(); 

    //Replace content with text area
    let text_area = document.createElement('textarea')
    text_area.id = 'edit_box'
    text_area.innerHTML = content
    text_area.rows = 4
    text_area.cols = 30
    text_area.setAttribute('required', "true")
    post_div.insertBefore(text_area, post_div.firstChild)
    let line_break = document.createElement('br')
    text_area.parentNode.insertBefore(line_break, text_area.nextSibling)


    let button = document.getElementById(`edit_${post_id}`)
    button.id = `save_${post_id}`
    button.onclick = () => save_post(post_id)
    button.innerHTML = "Save"

}


save_post = (post_id) => {
   let text_area = document.getElementById('edit_box').value

    //Save content 
    fetch(`/edit/${post_id}`, {
        method: "PUT", 
        body: JSON.stringify({
            content: text_area
        })
    })

    // Restore index view
    let post_div = document.getElementById(`post_div_${post_id}`)
    let area = post_div.children[0]
    area.remove() 


    let p = document.createElement('p')
    p.innerHTML = text_area
    post_div.insertBefore(p, post_div.firstChild)
    post_div.removeChild (p.nextSibling)

    let button = document.getElementById(`save_${post_id}`)
    button.id = `edit_${post_id}`
    button.onclick = () => edit_post(post_id)
    button.innerHTML = "Edit"
}

update_likes = post_id => {
    console.log(post_id)
    fetch (`/like/${post_id}`)
    .then (res => res.json())
    .then (data => {
        //update likes 
        let likes_selection = document.getElementById(`like_${post_id}`)
        const count = data['likes']
        likes_selection.innerHTML = `Likes: ${count}`


    })
}

like_post = post_id => {
    update_likes(post_id)

    let b = document.getElementById(`like_${post_id}`)
    b.id = `unlike_${post_id}`
    b.onclick = () => {
        unlike_post (post_id)
    }
    b.innerHTML = "Unlike"
    console.log(b)
}

unlike_post = post_id => {
    update_likes(post_id)

    let b = document.getElementById(`unlike_${post_id}`)
    b.id = `like_${post_id}`
    b.onclick = () => { 
        like_post(post_id)
    }
    console.log(b)
    b.innerHTML = "Like"
}