import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-robo',
  templateUrl: './robo.component.html',
  styleUrls: ['./robo.component.css']
})
export class RoboComponent {
  videoUrl: string = 'http://localhost:5000/video';
  urlInput: string = ''; // Adicionado para o campo de texto
  mouseX: number = 0;
  mouseY: number = 0;
  mouseEvent: string = '';
  lastKeyPressed: string = '';
  events: any[] = [];

  // Variáveis de estado para os botões
  gravando: boolean = false;
  executando: boolean = false;

  constructor(private http: HttpClient) {}

  accessUrl(): void {
    if (this.urlInput) {
      const endpoint = 'http://127.0.0.1:8000/open';
      const body = { url: this.urlInput };

      if(this.gravando){
        this.events.push({id:this.events.length, type:"open", url:this.urlInput, time:new Date().toISOString()});
      }

      this.http.post(endpoint, body).subscribe({
        next: () => {
          // Opcional: atualizar videoUrl ou mostrar mensagem de sucesso
          console.error('OPEN');
        },
        error: (err) => {
          // Opcional: tratar erro
          console.error('Erro ao acessar a URL:', err);
        }
      });
    }
  }

  onMouseMove(event: MouseEvent): void {
    const rect = (event.target as HTMLImageElement).getBoundingClientRect();
    this.mouseX = Math.floor(event.clientX - rect.left);
    this.mouseY = Math.floor(event.clientY - rect.top);

      if(this.gravando){
        //this.events.push({id:this.events.length, type:"MOUSE_MOVE", mouseX:this.mouseX, mouseY:this.mouseY, time:new Date().toISOString()});
      }
    //const url = `http://127.0.0.1:8000/move_mouse?x=${this.mouseX}&y=${this.mouseY}&duration=0`;
    //this.http.post(url, {}).subscribe();
  }

  onMouseDown(event: MouseEvent): void {
    const buttonMap: { [key: number]: string } = { 0: 'left', 1: 'middle', 2: 'right' };
    this.mouseEvent = buttonMap[event.button] || 'unknown';

      if(this.gravando){
        this.events.push({id:this.events.length, type:"MOUSE_DOWN", mouseX:this.mouseX, mouseY:this.mouseY, event:buttonMap[event.button], time:new Date().toISOString()});
      }
    
    const url = `http://127.0.0.1:8000/move_mouse_and_click?x=${this.mouseX}&y=${this.mouseY}&duration=0&event=${buttonMap[event.button]}`;
    this.http.post(url, {}).subscribe();
  }

  onKeyDown(event: KeyboardEvent): void {
    this.lastKeyPressed = event.key;
    console.log(this.lastKeyPressed);

      if(this.gravando){
        this.events.push({id:this.events.length, type:"KEY", lastKeyPressed:this.lastKeyPressed, time:new Date().toISOString()});
      }

    const url = `http://127.0.0.1:8000/press?key=${this.lastKeyPressed}`;
    this.http.post(url, {}).subscribe();
  }

  onMouseWheel(event: WheelEvent) {
    if (event.deltaY < 0) {
      console.log('Scroll para cima', event.deltaY);
    } else {
      console.log('Scroll para baixo', event.deltaY);
    }
      if(this.gravando){
        this.events.push({id:this.events.length, type:"MOUSE_WHEEL", deltaY:event.deltaY, time:new Date().toISOString()});
      }
    const url = `http://127.0.0.1:8000/scroll?deltaY=${event.deltaY}`;
    this.http.post(url, {}).subscribe();
  }

  onGravar(): void {
    this.gravando = true;
    this.executando = false;
    this.events = [];
    console.log('Gravar clicado');
  }

  onParar(): void {
    this.gravando = false;
    this.executando = false;
    console.log('Parar clicado');
  }

  onExecutar(): void {
    this.executando = true;
    this.gravando = false;
    console.log('Executar clicado');
  }

}
