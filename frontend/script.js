const API_BASE = 'http://localhost:8000';

let lastPlan = null;

document.getElementById('plan-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const prefs = {
    origin: fd.get('origin'),
    destination: fd.get('destination'),
    start_date: fd.get('start_date'),
    end_date: fd.get('end_date'),
    budget: Number(fd.get('budget')),
    party_size: Number(fd.get('party_size')),
    interests: (fd.get('interests') || '').split(',').map(s => s.trim()).filter(Boolean),
    mobility_needs: fd.get('mobility_needs') || null
  };
  const res = await fetch(`${API_BASE}/itinerary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ preferences: prefs })
  });
  const data = await res.json();
  lastPlan = { preferences: prefs, itinerary: data.itinerary };
  document.getElementById('plan-output').textContent = JSON.stringify(data, null, 2);
});

document.getElementById('explain-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const req = fd.get('request');
  const payload = { preferences: lastPlan?.preferences, current_itinerary: lastPlan?.itinerary, request: req };
  const res = await fetch(`${API_BASE}/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById('explain-output').textContent = JSON.stringify(data, null, 2);
});

document.getElementById('replan-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  if(!lastPlan){ alert('Generate a plan first.'); return; }
  const fd = new FormData(e.target);
  const sig = {
    type: fd.get('type'),
    message: fd.get('message') || '',
    data: sigDataFromType(fd.get('type'))
  };
  const payload = { preferences: lastPlan.preferences, current_itinerary: lastPlan.itinerary, signals: [sig] };
  const res = await fetch(`${API_BASE}/replan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  lastPlan.itinerary = data.itinerary;
  document.getElementById('replan-output').textContent = JSON.stringify(data, null, 2);
});

function sigDataFromType(t){
  if(t === 'transit_delay') return { delay: 20 };
  if(t === 'closure_notice') return { place_id: 'poi_001' };
  return {};
}
