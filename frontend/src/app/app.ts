import { Component, signal } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import {CommonModule} from "@angular/common";
import { RouterOutlet } from '@angular/router';
import { SubmissionPage } from './features/submission/submission.page/submission.page';
import { Demo } from "./demo/demo";
import { HttpClientModule } from '@angular/common/http';
import { EvaluateClientComponent } from './credit_decision/evaluate-client/evaluate-client';


@Component({
  selector: 'app-root',
  imports: [ RouterOutlet,  ReactiveFormsModule, CommonModule,HttpClientModule,EvaluateClientComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

