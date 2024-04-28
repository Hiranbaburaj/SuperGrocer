var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productID, 'Action:', action)
        console.log('user:', user)
        if(user === 'AnonymousUser'){
            console.log('Not Logged In')
        }
        else{
            updateUserOrder(productID, action)
        }
    })
}

function updateUserOrder(productID, action){
    console.log('User is Logged In')
    var url = '/buyer/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productID, 'Action': action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}