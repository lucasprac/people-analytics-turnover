import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PredictionService {
  private baseUrl = 'http://localhost:8000';
  constructor(private http: HttpClient) {}

  predict(payload: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/predict`, payload);
  }

  health(): Observable<any> {
    return this.http.get(`${this.baseUrl}/health`);
  }
}
