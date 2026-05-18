import { useState } from "react"
import { useEffect } from "react"
import { useRef } from "react"
import {
    Download
} from "lucide-react"
import {
    Upload,
    Music2,
    LogOut
} from "lucide-react"
import WaveformPlayer
from "../components/WaveformPlayer"
import MultiTrackPlayer
from "../components/MultiTrackPlayer"
import api from "../services/api"

export default function Dashboard() {
    const [errorMessage, setErrorMessage] =
    useState("")
        const [uploadedFilename,setUploadedFilename] =
        useState("")
        const waveRefs =
    useRef([])

    const [socket, setSocket] =
    useState(null)
    const [file, setFile] = useState(null)
    //const [uploading, setUploading] = useState(false)
    const [message, setMessage] = useState("")
    const [progress, setProgress] = useState(0)

    const [stems, setStems] = useState([])
    const [uploading, setUploading] = useState(false)
    const [connected, setConnected] =
    useState(false)
    const [progressText, setProgressText] =
    useState("")
    useEffect(() => {

    const ws = new WebSocket(
        "wss://stemstarserver-81vf.onrender.com/ws/progress"
    )
    ws.onerror = (error) => {

    console.error(
        "WebSocket error",
        error
    )
}   
    ws.onopen = () => {

    console.log(
        "WebSocket connected"
    )
    //alert("ready for upload")

    setConnected(true)

    setErrorMessage("")
}
    ws.onclose = () => {

    console.log(
        "WebSocket disconnected"
    )
    setTimeout(() => {

    //window.location.reload()

}, 2000)
}

ws.onmessage = (event) => {

    console.log("WS:", event.data)

    // Try JSON first
    try {

        const data =
            JSON.parse(event.data)

        // Completion message
        if (
            data.type === "complete"
        ) {

            console.log(
                "Received stems:",
                data.stems
            )

            setTimeout(() => {

                setStems(data.stems)

                localStorage.setItem(
                    "stems",
                    JSON.stringify(data.stems)
                )

                setProgress(100)

                setProgressText(
                    "Completed"
                )

                setUploading(false)

            }, 1000)
        }

        return

    } catch {

        // NOT JSON
        // so it's a Demucs log line
    }

    // Show processing logs
    setProgressText(
        event.data
    )

    // Parse REAL %
    const match =
        event.data.match(/^(\d+)%/)

    if (match) {

        setProgress(
            Number(match[1])
        )
    }
}
    setSocket(ws)

    return () => {

        ws.close()
    }

}, [])
useEffect(() => {

    const savedStems =
        localStorage.getItem(
            "stems"
        )

    if (savedStems) {

        setStems(
            JSON.parse(savedStems)
        )
    }

}, [])
    async function fetchStems(
    filename
) {

    try {

        const songName =
            filename.split(".")[0]

        const stemNames = [
            "vocals.wav",
            "drums.wav",
            "bass.wav",
            "other.wav"
        ]

        const generated =
            stemNames.map((stem) => ({

                name: stem,

                url:
                `http://127.0.0.1:8000/stems/${songName}/${stem}`
            }))

        setStems(generated)

    } catch (error) {

        console.error(error)

        setErrorMessage(
            "Failed to load stems"
        )

        setUploading(false)
    }
}

    async function handleUpload() {
        
    if (!file) {
        return
    }
    setUploadedFilename(
    file.name
)

    try {

        setUploading(true)
        setProgressText(
    "Preparing upload..."
)
        setProgress(0)
        setStems([])

        const formData = new FormData()

        formData.append(
            "file",
            file
        )

        const response = await api.post(
            "/upload",
            formData,
            {
                headers: {
                    "Content-Type":
                    "multipart/form-data"
                }
            }
        )
                    if (
                socket &&
                socket.readyState === WebSocket.OPEN
            ) {

                socket.send(file.name)

            } else {

                setErrorMessage(
                    "WebSocket not connected"
                )
            }




    } catch (error) {
    console.error(error)

    if (error.response) {

        setErrorMessage(
            "Backend error"
        )

    } else if (error.request) {

        setErrorMessage(
            "Server offline"
        )

    } else {

        setErrorMessage(
            "Unexpected error"
        )
    }

    setUploading(false)
}

    
}
    function handleLogout() {

        localStorage.removeItem("token")
        localStorage.removeItem(
    "stems"
)

        window.location.href = "/"
    }

    return (

        <div className="
            min-h-screen
            bg-gradient-to-br
            from-black
            via-zinc-950
            to-zinc-900
            text-white
        ">

            {/* Navbar */}

            <div className="
                flex
                items-center
                justify-between
                px-10
                py-6
                border-b
                border-zinc-800
            ">

                <div className="
                    flex
                    items-center
                    gap-3
                ">

                    <div className="
                        w-12
                        h-12
                        rounded-2xl
                        bg-white
                        flex
                        items-center
                        justify-center
                    ">
                        <Music2
                            className="text-black"
                            
                            
                        />
                    </div>

                    <div>

                        <h1 className="
                            text-2xl
                            font-bold
                            font-style
                            font-serif
                            font-extrabold
                            
                        ">
                            StemStar
                        </h1>

                        <p className="
                            text-zinc-400
                            text-sm
                            font-extrabold
                        ">
                            AI Stem Separation
                        </p>

                    </div>

                </div >
        <div className="
    relative
    bg-zinc-900
    rounded-3xl
">

    <button
        onClick={handleLogout}
        className="
            absolute
            top-2
            right-2

            flex
            items-center
            gap-4

            bg-zinc-800
            hover:bg-zinc-700

            transition
            px-4
            py-2
            rounded-xl
        "
    >
                    <LogOut size={24} />

                    Logout

                </button>
                </div>

            </div>

            {/* Content */}

            <div className="p-10">

                <h2 className="
                    text-5xl
                    font-bold
                ">
                    Dashboard
                </h2>

                <p className="
                    text-zinc-400
                    mt-3
                ">
                    Upload and separate your music stems
                </p>

                {/* Upload Area */}

                <div className="
                    mt-10
                    border-2
                    border-dashed
                    border-zinc-700
                    rounded-3xl
                    p-20
                    flex
                    flex-col
                    items-center
                    gap-6
                    bg-zinc-900/40
                ">

                    <Upload
                        size={60}
                        className="text-zinc-500"
                    />

                    <div className="text-center">

                        <h3 className="
                            text-2xl
                            font-semibold
                        ">
                            Upload Audio
                        </h3>

                        <p className="
                            text-zinc-500
                            mt-2
                        ">
                            MP3 / WAV supported
                        </p>

                    </div>

                    <input
                        type="file"
                        accept=".mp3,.wav"
                        onChange={(e) =>
                            setFile(e.target.files[0])
                        }
                        className="
                            text-sm
                            text-zinc-400
                            font-italic
                        "
                    />

                    {
                        file && (

                            <div className="
                                text-zinc-300
                            ">
                                {file.name}
                            </div>
                        )
                    }

                                <button
                onClick={handleUpload}
                disabled={uploading}
                className="
                    font-italic
                    bg-white
                    text-black
                    px-8
                    py-5
                    rounded-xl
                    font-semibold
                    hover:opacity-90
                    transition
                    disabled:opacity-50
                "
            >
                
                {
                    uploading
                    ? "Processing..."
                    : "UPLOAD"
                }
            </button>
            {
                    errorMessage && (

                        <div className="
                            text-red-400
                            mt-4
                            text-sm
                        ">

                            {errorMessage}

                        </div>
                    )
                }

{
    uploading && (

        <div className="
            w-full
            max-w-md
            mt-6
        ">

            <div className="
                flex
                justify-between
                text-sm
                text-zinc-400
                mb-2
            ">

                <span>
                    {progressText}
                </span>

                <span>
                    {progress}%
                </span>

            </div>

            <div className="
                w-full
                h-3
                bg-zinc-800
                rounded-full
                overflow-hidden
            ">

                <div
                    className="
                        h-full
                        bg-white
                        transition-all
                        duration-500
                    "
                    style={{
                        width: `${progress}%`
                    }}
                ></div>

            </div>

        </div>
    )
}


    {/* <button
    className="
        bg-white
        text-black
        px-4
        py-2
        rounded-xl
        font-semibold
        hover:opacity-90
        transition
    "
        onClick={() => {

            waveRefs.current.forEach(
    (ws) => {

        if (ws) {
            ws.play()
        }
    }
)
        }}
    >
        Play All
    </button>

    <button className="
    bg-zinc-800
    px-4
    py-2
    rounded-xl
    hover:bg-zinc-700
    transition
"
        onClick={() => {

            waveRefs.current.forEach(
    (ws) => {

        if (ws) {
            ws.pause()
        }
    }
)
        }}
    >
        Pause All
    </button>

</div> */}

{
    stems.length > 0 && (

        <>

            <div className="
                flex
                gap-4
                mb-8
            ">

                <button
                    className="
                        bg-white
                        text-black
                        px-4
                        py-2
                        rounded-xl
                        font-semibold
                        hover:opacity-90
                        transition
                    "
                    onClick={() => {

                        waveRefs.current.forEach(
                            (ws) => {

                                if (ws) {
                                    ws.play()
                                }
                            }
                        )
                    }}
                >
                    Play All
                </button>

                <button
                    className="
                        bg-zinc-800
                        px-4
                        py-2
                        rounded-xl
                        hover:bg-zinc-700
                        transition
                    "
                    onClick={() => {

                        waveRefs.current.forEach(
                            (ws) => {

                                if (ws) {
                                    ws.pause()
                                }
                            }
                        )
                    }}
                >
                    Pause All
                </button>

            </div>

            <div className="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-6
                mt-10
                w-full
            ">

                {
                    stems.map((stem, index) => (

                        <div
                            key={stem.name}
                            className="
                                bg-zinc-900
                                border
                                border-zinc-800
                                rounded-2xl
                                p-6
                            "
                        >

                                                    <div className="
                            flex
                            items-center
                            justify-between
                            mb-4
                        ">

                            <h3 className="
                                text-xl
                                font-semibold
                            ">
                                {stem.name}
                            </h3>

<button
    onClick={async () => {

        try {

            const response =
                await fetch(stem.url)

            const blob =
                await response.blob()

            const url =
                window.URL.createObjectURL(blob)

            const a =
                document.createElement("a")

            a.href = url

            a.download =
                stem.name

            document.body.appendChild(a)

            a.click()

            a.remove()

            window.URL.revokeObjectURL(url)

        } catch (error) {

            console.error(
                "Download failed",
                error
            )
        }
    }}    className="
        bg-zinc-800
        hover:bg-zinc-700
        transition-all
        duration-300
        p-3
        rounded-xl
        border
        border-zinc-700
        hover:scale-105
    "><Download size={18}></Download></button>

                        </div>

                            <WaveformPlayer
                                audioUrl={stem.url}
                                waveRefs={waveRefs}
                                index={index}
                            />

                        </div>
                    ))
                }

            </div>

        </>
    )
}
                    {
                        message && (

                            <div className="
                                text-zinc-400
                                mt-2
                            ">
                                {message}
                            </div>
                        )
                    }

                </div>

            </div>

        </div>
    )
}