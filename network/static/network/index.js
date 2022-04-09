document.addEventListener("DOMContentLoaded",() => {
    document.querySelector("#allpost").addEventListener('click', () => allpost());
    document.querySelector("#following").addEventListener('click', () => following());
    document.querySelector("#form-new-tweet").addEventListener("submit", () => {new_post(); });
    document.querySelector("#search").addEventListener("click", ()=>{searchUser(); return false});
    rundomFunc();
    userImgFunc();
    let GeneralID = "post-pack";
    let next = "next";
    let prev = "prev";
    show_list("/show_list", GeneralID, "1000000000000","1000000000002", "1000000000003", "1000000000004",next, prev);
});

const reloadUsingLocationHash = ()=>{
  window.location.hash = "reload";
};
// get user id
getUserId = (username) => {
  fetch("/get_user_id/"+username)
  .then(response => response.json())
  .then(result => {
    profile(username , result.id , result.email)
  });
};

// search user
function searchUser(){
  const username = document.querySelector("#searchInput").value;
  try{
    fetch("/get_user_id/"+username)
    .then(response => {
      if(response.ok){
        response.json()
        .then(result => {
          profile(username , result.id , result.email)
        });
      }else{
        document.querySelector("#searchInput").value="";
        document.querySelector("#random-follow").innerHTML=`
        <p style='color:red; font-weight:bold; margin:auto; font-size:20px;'><span style='color:blue; font-size:25px;'>${username}</span> not found </p>
        `
      }
    })
    .catch(console.log("not found"))
  }
  catch{
    document.querySelector("#searchInput").value="";
  }
  
    
}
// Start Profile Function
profile = (username , user_id , email) => {
    const kk = document.querySelector("#profile").textContent;
    const tt = kk.replace(/\s+/g, '');
    if(tt !== username){
      document.querySelector("#btn-ed").style.display="none";
    }
    document.querySelector("#home").style.display = 'none';
    document.querySelector("#following-page").style.display = 'none';
    document.querySelector("#profile-page").style.display = 'block';
    document.querySelector("#btn-ed").addEventListener("click", function(){
      document.querySelector("#edit-div").style.display = "block";
      document.querySelector("#profile-desc").style.display="none";
      document.querySelector("#img-src").addEventListener('change', event => { 
        const files = event.target.files
        
        document.querySelector("#save-edit-profile").addEventListener("click", () => {
          let formData = new FormData()
          const desc = document.querySelector("#edit-desc").value;
          formData.append("img",files[0]);
          formData.append("description",desc);
          formData.append("user",user_id);
          fetch("/ProfileView/"+user_id,{
            method:"POST",
            body: formData,
          })
          .then(response => response.json())
          .then(data => {
            document.querySelector("#edit-div").style.display = "none";
            document.querySelector("#profile-desc").style.display="block";
             giv();
            })
        })
      }) 
  
    })
    

    
    giv = () =>{
      fetch("/ProfileView/"+user_id).then(response => response.json()).then(result => {
        let imgSrc = result.img;
        document.querySelector("#profile-user").innerHTML=username;
        document.querySelector("#profile-email").innerHTML=email;
        document.querySelector("#profile-desc").innerHTML=result.description;
        document.querySelector("#profile-img").style.backgroundImage = `url(${imgSrc})`;
      });
    }
    giv();
    fetch("/follow/"+user_id).then(response => response.json()).then(f => {
      document.querySelector("#followers").innerHTML=`${f.followers} Followers`;
      document.querySelector("#follows").innerHTML=`${f.follows} Follows`;
    });

    fetch("/get_user_id/"+tt).then(response => response.json()).then(res => {
      
      rrr = () => {
          if(tt == username ){
            console.log("owner");
          }else{
            fetch("/unfollow/"+res.id+"/"+user_id).then(response => {
              if(response.ok){
                document.querySelector("#follow-btn").style.display= 'none';
                document.querySelector("#unfollow-btn").style.display= 'block';
                document.querySelector("#unfollow-btn").addEventListener("click", () => followed(user_id));
              }else{
                document.querySelector("#unfollow-btn").style.display= 'none';
                document.querySelector("#follow-btn").style.display= 'block';
                document.querySelector("#follow-btn").addEventListener("click", () => followed(user_id));
              }
            });
          }
        
      };
      
      rrr();
        
    });
      // follow function
    followed = (user_id) => {
      fetch("/get_user_id/"+tt).then(response => response.json()).then(res => {
        fetch("/unfollow/"+res.id+"/"+user_id).then(ponse => {
          if(ponse.ok){
            fetch("unfollow/"+res.id+"/"+user_id,{
              method: "DELETE"
            })
            .then(nse => {
              console.log("unfollowed");
            })
            .then(()=> {profile(username , user_id , email)})
          }else{
            fetch("/follow/"+user_id,{
              method: "POST",
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
              following:res.id,
              followed: user_id
              })
            })
            .then(se => se.json())
            .then(data => {
              console.log("followed");
              
            })
            .then(()=> {profile(username , user_id , email)})
          }
        })
      });   
    };
    
  //end follow function
  let idii = "postd-pack";
  let nextP ="nextP";
  let prevP = "prevP";
  show_list("/show_user_posts/"+user_id, "postd-pack", "5000000000000", "5000000000001", "5000000000002", "5000000000003",nextP, prevP);
};
// End Profile Function

// Start Show All Posts Function
allpost = () => {
    document.querySelector("#profile-page").style.display = 'none';
    document.querySelector("#following-page").style.display = 'none';
    document.querySelector("#home").style.display = 'block';
    
};
// End Show All Posts Function

// Start Show Following Posts Function
following = () => {
    document.querySelector("#profile-page").style.display = 'none';
    document.querySelector("#home").style.display = 'none';
    document.querySelector("#following-page").style.display = 'block';
    const kk = document.querySelector("#profile").textContent;
    const tt = kk.replace(/\s+/g, '');
    fetch("/get_user_id/"+tt).then(response => response.json()).then(res => {
      let dndn = "ppack";
      let nextF ="nextF";
      let prevF = "prevF";
      show_list("/show_following_posts/"+res.id, dndn, "8000000000008", "8000000000001", "8000000000002", "8000000000003",nextF,prevF);
      console.log(res.id);
    })
};
// End Show Following Posts Function

//random users function
rundomFunc = () => {
  const kk = document.querySelector("#profile").textContent;
  const tt = kk.replace(/\s+/g, '');
  fetch("/get_user_id/"+tt).then(response => response.json()).then(res => {
    fetch("/get_users_random/"+res.id).then(response => response.json()).then(data => {
      data.forEach(element => {
        fetch("/ProfileView/"+element.id)
        .then(response => response.json())
        .then(item => {
          const myDiv = document.createElement('div');
          const attr = document.createAttribute('class');
          attr.value = 'myDiv';
          myDiv.setAttributeNode(attr);
          document.querySelector('#random-follow').append(myDiv);
          myDiv.innerHTML = `
          <div class="d-flex justify-content-between parent align-items-center">
            <div style="cursor: pointer;" id="mask"><a href="javascript:getUserId('${element.username}')">${element.username}</a></div>
            <div style="max-height:60px; max-width:60px ;"><a href="javascript:getUserId('${element.username}')"><img class="p-1 im-pr" src="${item.img}" alt=""></a></div>
          </div>
        `
        })
      })
    })
  })
}

// end random users function
//show user img function
userImgFunc = () => {
  const kk = document.querySelector("#profile").textContent;
  const tt = kk.replace(/\s+/g, '');
  fetch("/get_user_id/"+tt).then(response => response.json()).then(res => {
        fetch("/ProfileView/"+res.id)
        .then(response => response.json())
        .then(item => {
          const imDiv = document.querySelector('#tweet-prof-img');
          imDiv.innerHTML = `
          <a href="javascript:getUserId('${item.username}')"><img class="p-1 im-pr" src="${item.img}" alt=""></a>
        `
        })  
  })
}

// show user img  function
// click edit post
function click_edit_post(post, saveID, dropD){
  document.querySelector("#p"+post+dropD).setAttribute("contenteditable","true");
  document.querySelector("#p"+post+dropD).focus();
  document.querySelector("#save"+saveID+post).style.display="block";
};
// edit post
function edit_post(post,user_id, saveID,dropD){
      const ola = document.querySelector("#p"+post+dropD).textContent;
      fetch("/show_post/"+post,{
          method:"PUT",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
          post:ola,
          user:user_id,
          })
      })
      .then(response => response.json())
      .then(result => {
        document.querySelector("#save"+saveID+post).style.display="none";
      });
};
// delete post
function delete_post(post, dropD){
  document.querySelector("#delete"+post+dropD).style.display="none";
  fetch("/show_post/"+post,{ method:"DELETE" })
  .then(response => {console.log("deleted")}) 
};


// Start Add New Post Function
function new_post(){
    const posty = document.querySelector("#textarea-post").value;
    const user = document.querySelector("#profile").textContent;
    const username = user.replace(/\s+/g, '');
    if(posty.length > 0 ){
        fetch("/show_list",{
            method:"POST",
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            post:posty,
            user:username
            })
        })
        .then(response => response.json())
        .then(result => {
          document.querySelector("#textarea-post").value = "";
        });
    };
};
// End Add New Post Function
 

// start the mother function of post

show_list = (url, idii, likeID, postID, saveID, dropD, next, prev) => {
  let userName = document.querySelector("#profile").textContent;
  let userNamePur = userName.replace(/\s+/g, '');
     fetch(url)
     .then(response => response.json())
     .then(result => {
        
        result.results.forEach(element => {
          // start get user img function
          getUserIimg = async () => {
            await fetch("/get_user_id/"+element.user)
              .then(response => response.json())
              .then(resu => {
                fetch("/ProfileView/"+resu.id)
                  .then(response => response.json())
                  .then(res => {
                        let d = element.date;
                        let myd = moment(d).fromNow();
                        let myDiv = document.createElement('div');
                        let attr = document.createAttribute('class');
                        attr.value = 'myDiv';
                        myDiv.setAttributeNode(attr);
                        document.querySelector('#'+idii).append(myDiv);
                        myDiv.innerHTML = `
                        <div class="post" id="delete${element.id}${dropD}">
                        <div class="post-profile d-flex justify-content-between parent align-items-center">
                        <div>
                        <img class="p-1 im-pr" src="${res.img}" alt="">
                        <div><span id="post-user"><a href="javascript:getUserId('${element.user}')">${element.user}</a></span></div>
                        </div>
                        <div class="dropdown" id="dropdowny${element.id}${dropD}">
                          <div style="margin-left: 40px; font-weight: normal;"><span><small>${myd}</small></span></div>
                        </div>
                        
                        </div>
                        <div class="post-body">
                        <p class="post-p" id="p${element.id}${dropD}">${element.post}</p>
                        <div class="d-flex justify-content-between parent">
                        <div class="like">
                         <button onClick="liked(${element.id},${resu.id},${likeID});" class="btn text-light bg-primary" id="like"><i class="fa-solid fa-heart"></i></button>
                         <span id="likes${likeID}${element.id}"></span>
                        </div>
                        <div class="save">
                         <button id="save${saveID}${element.id}" onClick="edit_post(${element.id},'${element.user}',${saveID},${dropD})" class="btn text-light bg-primary" style="display:none; font-weight: bold;">save</button>
                        </div>
                        <div class="comments">
                         <button id="showCmn${postID}${element.id}" onClick="show_comments(${element.id},${postID})" class="btn text-light bg-primary"><i class="fa fa-comment "></i></button>
                         <span id="comments${postID}${element.id}"></span>
                        </div>
                        </div>
                        <form id="commentForm" class="d-flex justify-content-between parent" onsubmit="return false">
                              <textarea id="comText${postID}${element.id}" class="comText" placeholder="leave..."></textarea>
                              <a href="javascript:newComment(${element.id},${postID})" style="margin-top: 3px; border:none; margin-left: 2px;" class="comInput">comment</a>
                        </form>
                          
                        <div class="displayComments" id="cmDiv${postID}${element.id}" style="display:none"></div>
                        
                        </div>
                        </div>
                        `
                      if(userNamePur == element.user){
                        let option = document.createElement('div');
                        document.querySelector('#dropdowny'+element.id+dropD).append(option);
                        option.innerHTML = `
                          <button style="color: #007bff;margin: auto;margin-left: 2px;border: none; float:right; margin-top: 8px;
                          outline: none; cursor:pointer;" class="dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <i class="fa fa-list" aria-hidden="true"></i>
                          </button>
                          <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item" href="javascript:click_edit_post(${element.id},${saveID},${dropD})"><i class="fa fa-edit" style="color:#007bff"></i>  Edit</a>
                            <a class="dropdown-item" href="javascript:delete_post(${element.id},${dropD})"><i class="fa fa-remove" style="color:red"></i>  Remove</a>
                          </div>
                          `
                      }
                      getlikes(element.id, likeID);
                      getCommentCount(element.id,postID); 
                  });
              });
             };
            getUserIimg();
        });

        // to control pagination 'next'
        if(result.next){
          document.querySelector('#'+next).style.display="block";
          document.querySelector('#'+next).innerHTML = `
            <button id='btnNext${next}' class='btn page-link'>next</button>
            `
            document.querySelector("#btnNext"+next).addEventListener("click",()=>{
              document.querySelector('#'+idii).innerHTML="";
              document.querySelector('#'+next).innerHTML="";
              show_list(result.next,idii, likeID, postID, saveID, dropD, next, prev) 
            })
          }
         // to control pagination 'previous'
        if(result.previous){
          document.querySelector('#'+prev).style.display="block";
          document.querySelector('#'+prev).innerHTML = `
            <button id='btnPrev${next}' class='btn page-link' >prev</button>
            `
            document.querySelector("#btnPrev"+next).addEventListener("click",()=>{
              document.querySelector('#'+idii).innerHTML="";
              document.querySelector('#'+prev).innerHTML="";
              show_list(result.previous,idii, likeID, postID, saveID, dropD, next,prev) 
            })
          }

        reloadUsingLocationHash();
    });
};


// end the mother function of post

// comment funcs
function getCommentCount(post, postID){
  fetch("/comments/"+post)
  .then(response => response.json())
  .then(cmn => {
    document.querySelector("#comments"+postID+post).innerHTML = cmn.counts;
  })
}
function newComment(post,postID){
  let comment = document.querySelector("#comText"+postID+post).value;
  let user = document.querySelector("#profile").textContent;
  let username = user.replace(/\s+/g, '');
    if(comment.length > 0 ){
      fetch("/comments/"+post,{
          method:"POST",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            body: comment,
            user: username,
            post: post,
          })
      })
      .then(response => response.json())
      .then(res => {
        document.querySelector("#comText"+postID+post).value = "";
        getCommentCount(post,postID);
        show_comments(post,postID);
        console.log(res)
  })
};
}
function show_comments(post, postID){
  document.querySelector("#cmDiv"+postID+post).style.display="block";
  fetch("/comments/"+post)
  .then(response => response.json())
  .then(result => {
    result.comnts.forEach(comment => {
      fetch("/get_user_id/"+comment.user)
      .then(response => response.json())
      .then(rt => {
        fetch("/ProfileView/"+rt.id)
        .then(response => response.json())
        .then(me => {
          const cmDiv = document.createElement('div');
          const attr = document.createAttribute('class');
          attr.value = 'cmDiv';
          cmDiv.setAttributeNode(attr);
          document.querySelector('#cmDiv'+postID+post).append(cmDiv);
          cmDiv.innerHTML = `
          <div class="comment">
            
            <a href="javascript:getUserId('${comment.user}')" class="post-profile d-flex justify-content-left parent align-items-center">
              <img src="${me.img}" style="width: 34px; height: 34px; border-radius: 50%;"/>
              <h6>${comment.user}</h6>
            </a>
            
            <p>${comment.body}</p>
          </div>
          `
          document.querySelector('#showCmn'+postID+post).addEventListener('click', () => {
            document.querySelector('#cmDiv'+postID+post).style.display = 'none';
          })
        })
      })
    })
  })
}
// end comments functions

// like functions
function getlikes(post,likeID){
  fetch("/like/"+post)
  .then(response => response.json())
  .then(re => {
     document.querySelector("#likes"+likeID+post).innerHTML=re.Likes;
  })
}

function liked(post_id,user_id,likeID){
    const user = document.querySelector("#profile").textContent;
    const username = user.replace(/\s+/g, '');
    fetch("/get_user_id/"+username)
   .then(response => response.json())
   .then(result => {
        fetch("/unlike/"+post_id+"/"+result.id).then(response => {
          if(response.ok){
            fetch("unlike/"+post_id+"/"+result.id,{
              method: "DELETE"
            })
            .then(response => {
              getlikes(post_id,likeID);
              console.log("unliked");
            })
          }else{
            fetch("/like/"+post_id,{
              method: "POST",
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
              user:result.id,
              post: post_id
              })
            })
            .then(response => response.json()).then(data => {
              console.log("liked");
              getlikes(post_id,likeID);
            });
          }
        
        })
    })
};
