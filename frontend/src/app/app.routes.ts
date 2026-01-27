import { Routes } from '@angular/router';
import { Outcome } from './outcome/outcome';
import { Audit } from './audit/audit';
import { Demo } from './demo/demo';
import { EvaluateClientComponent } from './credit_decision/evaluate-client/evaluate-client';
export const routes: Routes = [
    {path: 'outcome', component: Outcome, title: 'Outcome Update'},
    {path: 'audit', component: Audit, title: 'Audit Logs'},
    {path: 'demo', component: Demo, title: 'Demo'},
    { path: 'evaluate', component: EvaluateClientComponent }
];
