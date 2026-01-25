import { Routes } from '@angular/router';
import { Outcome } from './outcome/outcome';
import { Audit } from './audit/audit';
import { Demo } from './demo/demo';

export const routes: Routes = [
    {path: 'outcome', component: Outcome, title: 'Outcome Update'},
    {path: 'audit', component: Audit, title: 'Audit Logs'},
    {path: 'demo', component: Demo, title: 'Demo'}
];
