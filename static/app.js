// const parkInfo = $('#park-info')
// const likeBtn = $('.fave')
// parkInfo.on('click', '.fave', handleFavorite())

// async function handleFavorite(e) {
//     e.preventDefault()
//     const id = $(e.target).parent().data('id')
    
//     if (e.target.classList.contains('fas')) {
//         await axios.delete(`/favorite/${id}`)
//         $(e.target).toggleClass('fas fa-heart')
//         $(e.target).toggleClass('far fa-heart')
//     } else {
//         await axios.post(`/favorite/${id}`, (data = {id: id}))
//         $(e.target).toggleClass('fas fa-heart')
//         $(e.target).toggleClass('far fa-heart')
//     }
// }
// $(handleFavorite());

