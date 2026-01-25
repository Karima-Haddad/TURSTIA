import { Routes } from '@angular/router';
import { Outcome } from './outcome/outcome';
import { Audit } from './audit/audit';
import { Demo } from './demo/demo';
import { SubmissionPage } from './features/submission/submission.page/submission.page';

export const routes: Routes = [
    {path: 'outcome', component: Outcome, title: 'Outcome Update'},
    {path: 'audit', component: Audit, title: 'Audit Logs'},
    {path: 'demo', component: Demo, title: 'Demo'},
    {path: 'submission', component: SubmissionPage, title: 'Submission'}
];
