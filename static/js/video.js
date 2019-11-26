const video = document.getElementById('video')

    Promise.all(
            [
                faceapi.nets.tinyFaceDetector.loadFromUri('./static/weights'),
                faceapi.nets.faceLandmark68Net.loadFromUri('./static/weights'),
                faceapi.nets.faceRecognitionNet.loadFromUri('./static/weights'),
                faceapi.nets.faceExpressionNet.loadFromUri('./static/weights')
            ]
        ).then(startVideo)

    function startVideo() {
        navigator.getUserMedia(
            { video: {} },
            stream => video.srcObject = stream,
            error => console.error(error)
        )
    }

    video.addEventListener('play', () => {
        const canvas = faceapi.createCanvasFromMedia(video)
        document.body.append(canvas)
        const displaySize = {width : video.width, height: video.height}
        faceapi.matchDimensions(canvas, displaySize)
        setInterval(async () => {
            detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks()
                .withFaceExpressions()
            console.log(detections)
            const resizedDetections = faceapi.resizeResults(detections, displaySize)
            canvas.getContext('2d').clearRect(0,0,canvas.width, canvas.height)
            faceapi.draw.drawDetections(canvas, resizedDetections)
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
            faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
        }, 5000)
    });