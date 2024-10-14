import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  template: `
    <div class="app-container">
      <h1>Bienvenido a la Aplicación de Generación de Contenido</h1>
      <nav>
        <button routerLink="/evaluation-generator" class="options_generate">Ir al Generador de Evaluaciones</button>
        <button routerLink="/document-generator" class="options_generate">Ir al Generador de Documentos Word</button>
        <button routerLink="/presentation-generator" class="options_generate">Ir al Generador de Presentaciones</button>
      </nav>
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    h1 {
      text-align: center;
      color: #333;
    }
    .options_generate {
      margin: 5px;
    }
    nav {
      display: flex;
      justify-content: center;
      margin-bottom: 20px;
    }
  `]
})
export class AppComponent { }