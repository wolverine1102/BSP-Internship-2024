import * as d3 from 'd3';
import { XAxis } from 'recharts';


export default function CustomizedXAxis({ key }) {
  // Get today's date and set start/end times for the axis
  const today = new Date();
  const startTime = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 6, 0, 0);
  const endTime = new Date(startTime.getTime() + 24 * 60 * 60 * 1000); // Add 24 hours

  const xTicks = d3.timeHours(startTime, endTime, 1);
  const xTicksFormat = d3.timeFormat("%H:%M  %d/%m");

  return (
    <XAxis
      orientation="top"
      type="number"
      allowDataOverflow={true}
      domain={[startTime.getTime(), endTime.getTime()]}
      ticks={xTicks}
      scale={"time"}
      interval={0}
      tickFormatter={xTicksFormat}
      tick={{
        fontSize: "11px",
        fill: "#000000",
        dx: 75,
        letterSpacing: "2px",
        fontWeight: 700
      }}
      tickMargin={8}
      dataKey={key}
    />
  )
};


