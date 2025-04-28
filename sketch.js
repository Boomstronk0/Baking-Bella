let classifier,    // De classifier voor het ML-model
    port,          // De seriële poort
    writer,        // Writer om data naar de seriële poort te schrijven
    video,         // De videoinvoer
    flippedVideo,  // De gespiegeld videoinvoer
    label = '',    // Het label van de classificatie
    conf = 0;      // Het vertrouwen van de classificatie

async function setup() {
    // Maak het canvas voor de video en configureer de videoinvoer
    const canvas = createCanvas(320, 240);
    canvas.parent('canvasContainer');  // Plaats het canvas binnen het 'canvasContainer' element
    video = createCapture(VIDEO);
    video.size(320, 240);
    video.hide();

    // Laad het ML-model
    classifier = await ml5.imageClassifier('./image_model/model.json');
    classifyVideo();  // Start de classificatie van de video

    // Controleer of de Web Serial API beschikbaar is
    if ("serial" in navigator) {
        // Haal de knop uit de HTML en voeg een event listener toe
        const connectButton = document.getElementById('connectButton');
        connectButton.addEventListener('click', connectSerial);
    } else {
        console.error('Web Serial API wordt niet ondersteund in deze browser.');
        alert('Web Serial API wordt niet ondersteund in deze browser.');
    }
}

async function connectSerial() {
    try {
        // Vraag de gebruiker om een seriële poort te selecteren
        port = await navigator.serial.requestPort();
        // Open de seriële poort met de juiste opties
        await port.open({ baudRate: 115200 });  // Baudrate aangepast naar 115200
        writer = port.writable.getWriter();
        console.log('Seriële poort geopend');

        // Verberg de knop na verbinding
        const connectButton = document.getElementById('connectButton');
        connectButton.style.display = 'none';
    } catch (err) {
        console.error('Fout bij het openen van de seriële poort:', err);
    }
}

function draw() {
    background(220);
    flippedVideo = ml5.flipImage(video);
    image(flippedVideo, 0, 0);
    // Toon het label en de vertrouwen op het canvas (optioneel)
    fill(255);
    textSize(16);
    textAlign(CENTER);
    text(`${label} (${nf(conf * 100, 2, 1)}%)`, width / 2, height - 4);
}

async function classifyVideo() {
    flippedVideo = ml5.flipImage(video);
    const results = await classifier.classify(flippedVideo);
    gotResult(null, results);
    classifyVideo();  // Classificeer de volgende frame
}

function gotResult(error, results) {
    if (error) {
        console.error(error);
        return;
    }
    // Resultaat verwerken
    label = results[0].label;
    conf = results[0].confidence;

    // Update de labels op het scherm
    document.getElementById('resultLabel').innerText = `Resultaat: ${label}`;
    document.getElementById('confidenceLabel').innerText = `Zekerheid: ${(conf * 100).toFixed(1)}%`;

    // Stuur het resultaat naar de microcontroller via de seriële poort
    if (writer) {
        const data = new TextEncoder().encode(label + '\n');
        writer.write(data);
    }
}
