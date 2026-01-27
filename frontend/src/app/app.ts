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


@Component({
  selector: 'app-root',
  imports: [ RouterOutlet, SubmissionPage, ReactiveFormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

