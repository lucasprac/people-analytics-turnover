import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `<div class="container"><h1>People Analytics - Turnover</h1><app-risk-dashboard></app-risk-dashboard></div>`,
  styles: [`.container{padding:16px;font-family:Arial}`]
})
export class AppComponent {}
