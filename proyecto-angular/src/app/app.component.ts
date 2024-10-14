import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  template: `
    <div class="app-container">
<<<<<<< HEAD
      <h1>Bienvenido a la Aplicación de Generación de Contenido</h1>
      <nav>
        <button routerLink="/evaluation-generator" class="options_generate">Ir al Generador de Evaluaciones</button>
        <button routerLink="/document-generator" class="options_generate">Ir al Generador de Documentos Word</button>
        <button routerLink="/presentation-generator" class="options_generate">Ir al Generador de Presentaciones</button>
      </nav>
=======
      <div class="header">
        <div class="logo">
          <img src="images/logo.jpg" alt="Logo de la aplicación" width="100" height="100"/>
        </div>
        <div class="title">
          <h1>Bienvenido a la Aplicación de Generación de Evaluaciones</h1>
        </div>
      </div>
      <button routerLink="/evaluation-generator" class="options_generate">Ir al Generador de Evaluaciones</button>
      <button routerLink="/document-generator" class="options_generate">Ir al Generador de Documentos Word</button>
>>>>>>> a00246ab297ee86581d065a5d71aa47fab12423c
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
<<<<<<< HEAD
    nav {
      display: flex;
      justify-content: center;
      margin-bottom: 20px;
=======
    .app-container {
      text-align: center;
      padding: 20px;
    }

    .header {
      display: flex !important;
      align-items: center;
      justify-content: center;
      gap: 10px;
      max-width: 80%;
      margin: 0 auto;
    }

    .logo {
      width: 30% !important;
    }

    .title {
      width: 70% !important;
    }

    .options_generate {
      margin: 10px;
      padding: 10px 20px;
      font-size: 16px;
>>>>>>> a00246ab297ee86581d065a5d71aa47fab12423c
    }
  `]
})
export class AppComponent { }