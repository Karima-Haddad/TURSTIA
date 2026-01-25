import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root',
})
export class AuditService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // Tous les audits
  getAllAudits(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/audit`);
  }

  // Audits par case
  getAuditByCase(caseId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/audit?case_id=${caseId}`);
  }
}
