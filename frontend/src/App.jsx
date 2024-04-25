import ScheduleMonitor from './pages/ScheduleMonitor';


export default function App() {
  return (
    <div className='p-2 pl-2.5'>
      <div className='text-slate-800 text-2xl font-bold tracking-[2px]'>SMS Schedule Monitoring</div>
      <div>
        <ScheduleMonitor />
      </div>
    </div>
  )
}

