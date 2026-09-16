// NO-CLOUDFLARE FETCHER - QadamRozgar - Only Open Sites (No Cloudflare)
// Sites with 0 restrictions: FPSC, PPSC, PaperPK, Jobz.pk, Indeed RSS, WhatJobs, Jooble, BEOE, NJP, WhatJobs PK

const NO_CF_SOURCES = [
  { id: 'fpsc_official', name: 'FPSC Official', url: 'https://www.fpsc.gov.pk/', type: 'govt', cf: false, parser: 'fpsc', priority: 1 },
  { id: 'ppsc_official', name: 'PPSC Official', url: 'https://www.ppsc.gop.pk/', type: 'govt', cf: false, priority: 1 },
  { id: 'paperpk', name: 'PaperPK Govt', url: 'https://www.paperpk.com/jobs/', type: 'govt', cf: false, priority: 1 },
  { id: 'jobz_pk', name: 'Jobz.pk', url: 'https://www.jobz.pk/jobs/', type: 'mixed', cf: false, priority: 1 },
  { id: 'indeed_rss', name: 'Indeed PK RSS', url: 'https://pk.indeed.com/rss?q=jobs&l=Pakistan', type: 'rss', cf: false, priority: 1 },
  { id: 'whatjobs', name: 'WhatJobs PK', url: 'https://www.whatjobs.com/jobs-in-pakistan/', type: 'mixed', cf: false, priority: 2 },
  { id: 'jooble', name: 'Jooble PK', url: 'https://pk.jooble.org/jobs-pakistan', type: 'mixed', cf: false, priority: 2 },
  { id: 'beoe', name: 'BEOE Gulf', url: 'https://beoe.gov.pk/foreign-jobs', type: 'gulf', cf: false, priority: 1 },
  { id: 'njp', name: 'NJP Govt', url: 'https://njp.gov.pk/', type: 'govt', cf: false, priority: 1 },
  { id: 'mustakbil_no_cf', name: 'Mustakbil No-CF Mirror', url: 'https://www.paperpkjobs.com/', type: 'private', cf: false, priority: 2 },
  { id: 'jobz_gulf', name: 'Jobz Gulf', url: 'https://www.jobz.pk/gulf-jobs/', type: 'gulf', cf: false, priority: 2 }
];

async function fetchNoCF(source){
  try {
    console.log(`[NO-CF] Fetching ${source.name} - ${source.url} - No Cloudflare`);
    const res = await fetch(source.url, { 
      headers: { 'User-Agent': 'Mozilla/5.0' },
      cache: 'no-store'
    });
    if(!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    if(text.length < 500) throw new Error('Too short');
    console.log(`[NO-CF] ✅ ${source.name} - ${text.length} chars - SUCCESS`);
    return { success: true, data: text, source };
  } catch(e){
    console.warn(`[NO-CF] ❌ ${source.name} failed: ${e.message}`);
    return { success: false, error: e.message, source };
  }
}

async function fetchFromNoCFRotation(){
  const rot = parseInt(localStorage.getItem('qr_no_cf_rot')||'0');
  const start = rot % NO_CF_SOURCES.length;
  console.log(`[NO-CF Rotation] Starting from index ${start} - ${NO_CF_SOURCES[start].name}`);
  
  for(let i=0; i<NO_CF_SOURCES.length; i++){
    const idx = (start + i) % NO_CF_SOURCES.length;
    const src = NO_CF_SOURCES[idx];
    const result = await fetchNoCF(src);
    if(result.success){
      localStorage.setItem('qr_no_cf_rot', (rot+1).toString());
      localStorage.setItem('qr_last_no_cf_source', src.name);
      // Update live counter
      document.getElementById('liveCounter') && (document.getElementById('liveCounter').textContent = `LIVE • ${src.name} • No Cloudflare • Just now`);
      return result;
    }
  }
  console.warn('[NO-CF] All NO-CF sources failed, fallback to EMBEDDED_JOBS');
  return { success: false, fallback: true };
}

window.fetchFromNoCFRotation = fetchFromNoCFRotation;
window.NO_CF_SOURCES = NO_CF_SOURCES;

// Auto start every 10 min
setInterval(fetchFromNoCFRotation, 10*60*1000);
setTimeout(fetchFromNoCFRotation, 2000);
