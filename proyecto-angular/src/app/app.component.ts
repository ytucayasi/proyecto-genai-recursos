import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  template: `
    <div class="app-container">
      <h1>Bienvenido a la Aplicación de Generación de Evaluaciones</h1>
      <button routerLink="/evaluation-generator">Ir al Generador de Evaluaciones</button>
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    h1 {
      text-align: center;
      color: #333;
    }
  `]
})
export class AppComponent { }