import { Routes } from '@angular/router';
import { Outcome } from './outcome/outcome';
import { Audit } from './audit/audit';
import { Demo } from './demo/demo';
import { SubmissionPage } from './features/submission/submission.page/submission.page';
import { Login } from './login/login';
import { AuthGuard } from './guards/auth';
import { SimilarityRadar } from './similarity-radar/similarity-radar';
import { EvaluateClientComponent } from './credit_decision/evaluate-client/evaluate-client';

export const routes: Routes = [
    {path: 'login', component: Login, title: 'Login'},
    {path: 'outcome', component: Outcome, title: 'Outcome Update', canActivate: [AuthGuard]},
    {path: 'audit', component: Audit, title: 'Audit Logs', canActivate: [AuthGuard]},
    {path: 'demo', component: Demo, title: 'Demo'},
    {path: 'submission', component: SubmissionPage, title: 'Submission'},
    {path:'similarity', component: SimilarityRadar, title:"Similarity radar"},
    { path: 'evaluate', component: EvaluateClientComponent }

]