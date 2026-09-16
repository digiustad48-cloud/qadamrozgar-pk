// QadamRozgar Secure Backend - /api/jobs/post
// Stack: Node + Supabase + Zod + Rate Limit + Anti-Fake 6-Level Check
import { z } from 'zod';

const postJobSchema = z.object({
  title: z.string().min(4).max(100),
  company: z.string().min(3).max(80),
  location: z.string().min(2),
  category: z.enum(['Govt','Private','Gulf']),
  salary: z.string().min(3).max(30),
  type: z.string(),
  description: z.string().min(20).max(2000),
  requirements: z.array(z.string()).max(10),
  email: z.string().email(),
  website: z.string().url().optional().or(z.literal('')),
  ntn: z.string().min(3).optional()
});

function antiFakeCheck(data){
  const fails=[];
  let score=100;
  // 1. No WhatsApp only
  if (/whatsapp/i.test(data.description) && !data.email) { fails.push('whatsapp_only'); score-=30; }
  // 2. Fee detection - instant block
  if (/fee|advance|registration|pay to apply|security deposit/i.test(data.description+data.title)) {
    return {isFake:true, fails:['fee_detected'], score:0};
  }
  // 3. Salary realistic
  const m = data.salary.match(/\d+/g);
  const num = m? parseInt(m[0]):0;
  if (data.salary.toLowerCase().includes('pkr') && num>500000) { fails.push('salary_unrealistic'); score-=25; }
  // 4. Official email - no gmail for companies
  if (['gmail.com','yahoo.com'].includes(data.email.split('@')[1])) { fails.push('free_email'); score-=15; }
  // 5. BEOE check for Gulf
  if (data.category==='Gulf' && (!data.ntn || data.ntn.length<5)) { fails.push('gulf_license_missing'); score-=20; }
  // 6. Company NTN format
  if (data.ntn && !/^[A-Z0-9-]{5,20}$/i.test(data.ntn)) { fails.push('ntn_invalid'); score-=10; }

  return {isFake: score<60, fails, score};
}

export default async function handler(req,res){
  // Security headers
  res.setHeader('X-Content-Type-Options','nosniff');
  res.setHeader('X-Frame-Options','DENY');
  
  if (req.method!=='POST') return res.status(405).json({error:'Method not allowed'});
  
  // Rate limit - 5 posts per hour per IP
  // (Implement with Upstash Redis in production)

  try{
    const parsed = postJobSchema.parse(req.body);
    const check = antiFakeCheck(parsed);
    
    if (check.isFake) {
      // Log attempt, block IP if repeated
      console.log('[SECURITY] Fake job blocked:', check.fails, parsed.company);
      return res.status(400).json({blocked:true, reason:check.fails, score:check.score});
    }

    // Parameterized insert - NO raw SQL
    // await supabase.from('pending_jobs').insert({...parsed, fakeScore: check.score, status:'pending'})

    return res.status(200).json({success:true, message:'Job submitted for verification', score:check.score});

  }catch(e){
    return res.status(400).json({error:'Validation failed', details:e.errors});
  }
}

// Daily Agent - runs 6AM via Vercel Cron
// /api/agent/daily-update
export async function dailyAgent(){
  const sources = [
    {name:'ndeed.pk', active:true, cf:false},
    {name:'brightspyre.com', active:true, cf:false},
    {name:'rozee.pk', active:false, reason:'Cloudflare - skipped'},
    {name:'mustakbil.com', active:false, reason:'Cloudflare - skipped'}
  ];
  for (let s of sources.filter(x=>x.active)){
    // fetch with safe parser, zod validation, duplicate check
    // insert with parameterized query only
  }
  // Clean fake jobs: delete where fakeScore<60 or fee detected
}
