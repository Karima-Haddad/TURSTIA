// Service pour gérer les résultats des dossiers

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OutcomeService {

  private API_URL = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  submitOutcome(payload: {
    case_id: string;
    outcome: string;
    loss_amount?: number;
  }): Observable<any> {
    return this.http.post(`${this.API_URL}/outcome`, payload);
  }
}
