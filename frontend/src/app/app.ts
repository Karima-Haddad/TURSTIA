import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
<<<<<<< HEAD
import { CommonModule } from '@angular/common';
import { Header } from './header/header';
import { Footer } from './footer/footer';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ RouterOutlet, CommonModule, Header, Footer],
=======
import { SubmissionPage } from './features/submission/submission.page/submission.page';
import { Demo } from "./demo/demo";
import { HttpClientModule } from '@angular/common/http';
import { EvaluateClientComponent } from './credit_decision/evaluate-client/evaluate-client';


@Component({
  selector: 'app-root',
  imports: [ RouterOutlet,  ReactiveFormsModule, CommonModule,HttpClientModule,EvaluateClientComponent],
>>>>>>> featnour
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

