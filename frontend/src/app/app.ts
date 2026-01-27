import { Component, signal } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import {CommonModule} from "@angular/common";
import { RouterOutlet } from '@angular/router';
import { SubmissionPage } from './features/submission/submission.page/submission.page';
import { FraudTestComponent } from './fraud-test/fraud-test';
import { FraudBannerComponent} from './fraud-banner/fraud-banner';
import { ColdStartWarningCardComponent } from './cold-start-warning-card/cold-start-warning-card';
import { AuditTimelineComponent } from './audit-timeline/audit-timeline';
@Component({
  selector: 'app-root',
  imports: [ RouterOutlet, SubmissionPage, ReactiveFormsModule, CommonModule, FraudTestComponent, FraudBannerComponent, ColdStartWarningCardComponent, AuditTimelineComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

