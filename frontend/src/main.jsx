import React,{useEffect,useState} from 'react'
import {createRoot} from 'react-dom/client'
import {LineChart,Line,XAxis,YAxis,Tooltip,ResponsiveContainer,CartesianGrid} from 'recharts'
import './styles.css'

const API='http://localhost:8000'
function Card({title,value,sub}){return <div className="card"><span>{title}</span><strong>{value}</strong><small>{sub}</small></div>}
function App(){
 const [summary,setSummary]=useState(null),[forecast,setForecast]=useState(null),[decision,setDecision]=useState(null),[scenario,setScenario]=useState(null),[inv,setInv]=useState(15),[busy,setBusy]=useState(false)
 useEffect(()=>{Promise.all([fetch(API+'/api/summary').then(r=>r.json()),fetch(API+'/api/forecast').then(r=>r.json())]).then(([s,f])=>{setSummary(s);setForecast(f)})},[])
 const runDecision=async()=>{setBusy(true);const r=await fetch(API+'/api/decision',{method:'POST'}).then(r=>r.json());setDecision(r);setBusy(false)}
 const runScenario=async()=>{const r=await fetch(API+'/api/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({inventory_delta:inv/100,price_delta:0,marketing_delta:0})}).then(r=>r.json());setScenario(r.result.evidence[0])}
 return <main>
  <header><div><div className="eyebrow">ENTERPRISE AI · DECISION INTELLIGENCE</div><h1>DecisionOS</h1><p>From data → evidence → decision.</p></div><button onClick={runDecision}>{busy?'Running agents…':'Run AI Decision Workflow'}</button></header>
  <section className="grid">{summary&&<><Card title="Total revenue" value={'$'+(summary.total_revenue/1e6).toFixed(2)+'M'} sub="Synthetic enterprise dataset"/><Card title="Avg daily revenue" value={'$'+Math.round(summary.average_daily_revenue/1000)+'K'} sub={'Through '+summary.latest_date}/><Card title="Data quality" value={summary.quality.status} sub={`${summary.quality.rows.toLocaleString()} rows`}/></>}</section>
  <section className="panel"><div className="panel-head"><div><h2>14-Day Revenue Forecast</h2><p>Random Forest regression with lagged KPI features</p></div>{forecast&&<div className="metric">R² {forecast.metrics.r2.toFixed(3)}</div>}</div>{forecast&&<ResponsiveContainer width="100%" height={300}><LineChart data={forecast.forecast}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="date"/><YAxis tickFormatter={v=>'$'+Math.round(v/1000)+'k'}/><Tooltip formatter={v=>'$'+Math.round(v).toLocaleString()}/><Line type="monotone" dataKey="revenue" strokeWidth={3}/></LineChart></ResponsiveContainer>}</section>
  <section className="two"><div className="panel"><h2>What-if Simulator</h2><p>Test an inventory intervention before acting.</p><label>Inventory change: <b>{inv}%</b></label><input type="range" min="-30" max="40" value={inv} onChange={e=>setInv(+e.target.value)}/><button className="secondary" onClick={runScenario}>Run Scenario</button>{scenario&&<div className="result"><b>{scenario.estimated_change_pct}%</b> estimated daily revenue change<br/><span>${scenario.baseline_daily_revenue.toLocaleString()} → ${scenario.projected_daily_revenue.toLocaleString()}</span></div>}</div>
  <div className="panel"><h2>Agent Trace</h2><p>Evidence-first orchestration chain</p>{decision?<div className="trace">{decision.trace.map((x,i)=><div key={i}><span>{String(i+1).padStart(2,'0')}</span><b>{x.agent}</b><small>{x.action}</small></div>)}</div>:<div className="empty">Run the workflow to generate an auditable trace.</div>}</div></section>
  {decision&&<section className="panel decision"><h2>Decision Output</h2><p>{decision.decision.headline}</p><ul>{decision.decision.actions.map((a,i)=><li key={i}>{a}</li>)}</ul></section>}
  <footer>DecisionOS · reproducible synthetic-data portfolio project · evidence over hype</footer>
 </main>
}
createRoot(document.getElementById('root')).render(<App/>)
