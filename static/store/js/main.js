var updateButtons = document.getElementsByClassName('update-cart')

for (i = 0; i < updateButtons.length; i++){
    updateButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('product ID:', productId, 'action:', action)
    

    console.log('User:', user)
    if(user==='AnonymousUser'){
        addCoookieItem(productId, action)
    }
    else{
        updateUserOrder(productId, action)
    }
    })
}

function addCoookieItem(productId, action){
    console.log('User is not at all logged in')
    if (action=='add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'remove'){
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0){
            console.log('item should be deleted')
            delete cart[productId];
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function updateUserOrder(productId, action){
    console.log('User is logged In')

    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    
    .then((response) =>{
        return response.json()
    })
    
    .then((data) =>{
        location.reload()
        return console.log('Data:', data)
    })
    
}