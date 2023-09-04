import React, { useEffect, useImperativeHandle, useRef, useState } from "react";
import SimpleWhiteBoard from "simple-white-board";
import Controls from "./Controls";
import axios from 'axios';
const DefaultSpinner = require('./DefaultSpinner').default;
const LatexWindow = require('./LatexWindow').default;
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export interface ReactSimpleWhiteBoardProps {
}

const sampleLatex = String.raw`\begin{align*}
a^2 + b^2 &= c^2 \\
a_5 - 3 &= \frac{b}{c}
\end{align*}`

const ReactSimpleWhiteBoard = React.forwardRef<HTMLCanvasElement>((props: ReactSimpleWhiteBoardProps, ref) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const whiteBoard = useRef<SimpleWhiteBoard>();
  const [canvasWidth, setCanvasWidth] = useState<number>(Math.min(window.innerHeight*0.8, window.innerWidth * 0.6));
  const [lineWidth, setLineWidth] = useState(3);
  const [lineColor, setLineColor] = useState("#000000");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [latexCode, setLatexCode] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useImperativeHandle(ref, () => canvasRef.current as HTMLCanvasElement, []);

  // useEffect(() => {
  //   const width = Math.min(
  //     typeof window !== "undefined" ? window.innerWidth * 0.6 : 500,
  //     500
  //   );
  //   setCanvasWidth(window.innerWidth * 0.6);
  // }, []);

  useEffect(() => {
    // I think this is run when the canvas is first created
    if (!canvasRef.current) return;
    whiteBoard.current = new SimpleWhiteBoard(canvasRef.current);
    setWhite();
    whiteBoard.current.setLineColor(lineColor);
    whiteBoard.current.setLineWidth(lineWidth);
    return () => {
      if (whiteBoard.current) {
        whiteBoard.current.dispose();
      }
    }
  }, [canvasWidth]);

  useEffect(() => {
    if (!whiteBoard.current) return;
    whiteBoard.current.setLineColor(lineColor);
    whiteBoard.current.setLineWidth(lineWidth);
  }, [lineColor, lineWidth]);

  const saveImage = () => {
    const canvas = canvasRef.current;
    const ctx = canvasRef.current?.getContext('2d');
    if (canvas != null && ctx != null) {
      let dataURL = canvas.toDataURL("image/png", 1.0);
      downloadImage(dataURL, 'my-canvas.png');
      console.log(dataURL)
    }
  }

  function downloadImage(data: any, filename = 'untitled.png') {
    let a = document.createElement('a');
    a.href = data;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
  }

  const setWhite = () => {
    const canvas = canvasRef.current;
    const ctx = canvasRef.current?.getContext('2d');
    ctx!.fillStyle = 'white';
    ctx!.fillRect(0, 0, canvas!.width, canvas!.height);
  }

  const handleFileChange = (e: any) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    const canvas = canvasRef.current;
    const image = new Image();
    image.src = URL.createObjectURL(file);
    image.onload = () => {
      const ctx = canvasRef.current?.getContext('2d');
      ctx?.drawImage(image, 0, 0, canvas!.width, canvas!.height)
    }
  }

  const sendImage = async () => {
    setIsLoading(true);
    try {
      let res = null;
      const canvas = canvasRef.current;
      const ctx = canvasRef.current?.getContext('2d');
      if (canvas != null && ctx != null) {
        let dataURL = canvas.toDataURL("image/png", 1.0);
        const response = await fetch(dataURL);
        const blob = await response.blob();
        console.log("loading")
        const formData = new FormData();
        formData.append("image", blob, 'image.png');
        res = await axios.post('https://www.muvision.ca/muvision/classify_image/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        })
        if(res.data != null){
          console.log(typeof(res.data));
          setLatexCode(res.data);
        }
        console.log(res.data);
      }else{
        await new Promise(r => setTimeout(r, 1000));
        setLatexCode(sampleLatex);
      }

      //await new Promise(r => setTimeout(r, 1000));
      //setLatexCode(sampleLatex);

    } catch (error) {
      alert(error)
      console.log(error)
      setIsLoading(false)
    }
    setIsLoading(false)
    
  }

  return (
    <>
      <h1 className="font-bold text-2xl mt-4 mb-2">Try out MuVision!</h1>
      <div className="react-simple-white-board">
        <Controls
          lineColor={lineColor}
          lineWidth={lineWidth}
          setLineColor={setLineColor}
          setLineWidth={setLineWidth}
        />
        <div className="flex">
          <canvas
            ref={canvasRef}
            width={window.innerWidth*0.6}
            height={window.innerHeight*0.7}
            className = "border-2 border-theme-stroke rounded-md"
          />
          {/* <LatexWindow code="$$(3\times 4) \div (5-2)$$"/> */}
        <LatexWindow code={latexCode} />
        </div>
        <div>
          <button className="bg-theme hover:bg-theme-stroke text-white font-bold py-2 px-4 rounded my-2 mx-1 hover:font-bold hover:scale-110 transform transition ease-in-out duration-150" onClick={() => {whiteBoard.current?.erase(); setWhite()}}>Clear drawing</button>
          <button className="bg-theme hover:bg-theme-stroke text-white font-bold py-2 px-4 rounded my-2 mx-1 hover:font-bold hover:scale-110 transform transition ease-in-out duration-150"
          onClick={saveImage}>Save drawing</button>
          <button className="bg-theme hover:bg-theme-stroke text-white font-bold py-2 px-4 rounded my-2 mx-1 hover:font-bold hover:scale-110 transform transition ease-in-out duration-150">
            <label htmlFor="upload-button" className="upload-button">
              Upload Image
            </label>
            <input
              type="file"
              id="upload-button"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
          </button>
          {selectedFile && <span>{selectedFile.name}</span>}

          <button disabled={isLoading} onClick={sendImage} className="bg-theme hover:bg-theme-stroke text-white font-bold py-2 px-4 rounded my-2 mx-1 hover:font-bold hover:scale-110 transform transition ease-in-out duration-150">
            {isLoading ? <p>Loading...</p> : <p>Submit drawing </p>}
          </button>
        </div>
      </div>
    </>
  );
});

export default ReactSimpleWhiteBoard;