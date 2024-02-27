// *****************
// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}
// *****************

var ques = document.getElementsByClassName("quesclass");
var answer = document.getElementsByClassName("answerclass");
// var ques = document.getElementById("question");
// var answer = document.getElementById("answer");

// function sendData() {
//     var data= [];
    
//     for(var i=0; i < ques.length; i++) {
//         var qna = {}
//         qna['question'] = ques[i].innerText;
//         qna['answer'] = answer[i].value
//         data.push(qna)
//     }
//     postData('/answer2db', data)
//         .then(xz => {
//             console.log(xz); // JSON data parsed by `data.json()` call
//         });
// }

function sendData(mykey) {
    var key = +mykey
    var data= [];
    
    var qna = {}
    qna['question'] = ques[key].innerText;
    qna['answer'] = answer[key].value
    data.push(qna)
    
    postData('/answer2db', data)
        .then(xz => {
            console.log(xz); // JSON data parsed by `data.json()` call
        });
}



// timer
var timelimit = 30  // in minutes

function countdown( elementName, minutes, seconds )
{
    var element, endTime, hours, mins, msLeft, time;

    function twoDigits( n )
    {
        return (n <= 9 ? "0" + n : n);
    }

    function updateTimer()
    {
        msLeft = endTime - (+new Date);
        if ( msLeft < 1000 ) {
            element.innerHTML = "countdown's over!";
        } else {
            time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
        }
    }

    element = document.getElementById( elementName );
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    updateTimer();
}

countdown( "countdown", timelimit, 0 ); 


setTimeout(function () { 
    var mybtn = document.getElementById("btnSubmitid");
    mybtn.click() 
}, timelimit*60*1000)




