const video = document.getElementById('video');

// Queue class
class Queue {
    // Array is used to implement a Queue
    constructor() {
        this.items = [];
    }

    // Functions to be implemented
    enqueue(element) {
        // adding element to the queue
        this.items.push(element);
    }

    // dequeue function
    dequeue() {
        // removing element from the queue
        // returns underflow when called
        // on empty queue
        if (this.isEmpty())
            return "Underflow";
        return this.items.shift();
    }

    // front()
    // isEmpty function
    isEmpty() {
        // return true if the queue is empty.
        return this.items.length == 0;
    }

    // printQueue()
}

Promise.all(
    [
        faceapi.nets.tinyFaceDetector.loadFromUri('./static/weights')
    ]
).then(startVideo)

function startVideo() {
    navigator.getUserMedia(
        {video: {}},
        stream => video.srcObject = stream,
        error => console.error(error)
    )
}

video.addEventListener('play', () => {
    const canvas = faceapi.createCanvasFromMedia(document.getElementById('video'))
    canvas.setAttribute("style", "z-index:1; position:absolute")
    document.body.append(canvas)
    const displaySize = {width: video.width, height: video.height}
    faceapi.matchDimensions(canvas, displaySize)
    var options = new faceapi.TinyFaceDetectorOptions();
    setInterval(async() => {
        console.log("in async");
        console.log(Date.now());
        let detections = await faceapi.detectAllFaces(video, options);
        console.log(detections)
        for(var i in detections) {
            let sendimage = false;
            if (!!detections[i] && detections[i]['score'] > 0.4) {
                // console.log(detections);
                sendimage = true;
                /*make ajax call (send the detections and current queue -> response contains friend name and confidence, if friend not in queue already)
                await classify(detections[i]['descriptor']);
                let friend = document.getElementById('friend').innerText;
                console.log('Friend is set to :' + friend);
                let shouldEnqueue = true;
                if(!queue.isEmpty()) {
                    for (var c in queue.items) {
                        if(queue['items'][c]['friend'] === friend) {
                            shouldEnqueue = false;
                        }
                    }
                }
                if(shouldEnqueue && friend) {
                    console.log("sending data to server");
                    test();
                    console.log(friend);
                    queue.enqueue({'friend': friend, 'timestamp': Date.now()})
                }
                */
            }
            if(sendimage) {
                document.getElementById("timestamp").innerText = Date.now().toString();
                console.log("Sending image to server");
                test()
            }
        }
    }, 2000)// wait 2 seconds before giving new inputs to model
});