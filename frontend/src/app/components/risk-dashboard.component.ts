import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-risk-dashboard',
  template: `
  <div>
    <h2>Dashboard de Risco</h2>
    <p>Conecte a API em http://localhost:8000</p>
  </div>
  `,
  styles: [``]
})
export class RiskDashboardComponent implements OnInit {
  constructor(private http: HttpClient) {}
  ngOnInit(): void {}
}
