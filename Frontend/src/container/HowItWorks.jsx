import React from 'react'

const HowItWorks = () => {
  return (
    <div>
      <div id="howitworks">features</div>
      <h1 className="text-2xl font-bold mt-5">How It Works</h1>
      <div className="bg-theme border border-theme-stroke flex justify-items-center rounded-xl p-6 my-2">
        <p className="text-white">
          MuVision uses the power of OpenCV to scan your image and extract the lines of math expressions. 📸
          Then, our algorithm splits each line into individual characters with bounding boxes. 🔲
          Each character is then fed into our amazing ensemble neural network, which can recognize any symbol or letter in your writing. 🤖
          Our ensemble model combines the best of both worlds: our own custom Tensorflow model, and several state-of-the-art pretrained models such as Resnet-50, VGG-19, and MobileNet. 🚀
          By taking a weighted average of their results, we can achieve high accuracy and robustness. 💯
          Finally, we use the PyLatex library to convert the text into Latex code, which you can copy and paste into your documents. 📝 <br />  <br />
          MuVision makes math easy and fun! 😊 We hope you enjoy using MuVision! 🙌
        </p>
      </div>
      
    </div>
  )
}

export default HowItWorks