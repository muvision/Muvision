import React from "react";

export interface Props {
  lineColor: string;
  setLineColor: any;
  lineWidth: any;
  setLineWidth: any;
}

export default function Controls(props: Props) {
  const { lineColor, setLineColor, lineWidth, setLineWidth } = props;

  return (
    <div className="react-simple-white-board-settings">
      {/* <div className="react-simple-white-board-control">
        <label style={{ marginRight: 10 }}>Brush Color</label>
        <input
          type="color"
          value={lineColor}
          onChange={(event) => {
            setLineColor(event.target.value);
          }}
        />
      </div> */}
      <div className="react-simple-white-board-control">
        {/* <label style={{ marginRight: 10 }}>Brush Width</label> */}
        {/* <input
          type="range"
          min="1"
          max="50"
          value={lineWidth}
          onChange={(event) => {
            setLineWidth(event.target.value);
          }}
        /> */}
      </div>
    </div>
  );
};