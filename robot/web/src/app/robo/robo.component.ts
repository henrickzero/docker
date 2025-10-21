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
  textInput: string = '';
  hotKeyInput: string = '';
  keyInput: string = '';
  mouseX: number = 0;
  mouseY: number = 0;
  duration: number = 0;
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
        },
        error: (err) => {
          // Opcional: tratar erro
          console.error('Erro ao acessar a URL:', err);
        }
      });
    }
  }

  sendHotKey(): void {
    if (this.hotKeyInput) {
      const endpoint = `http://127.0.0.1:8000/hotkey?key=${this.hotKeyInput}`;
      const body = { text: this.hotKeyInput };

      if(this.gravando){
        this.events.push({id:this.events.length, type:"hotkey", text:this.hotKeyInput, time:new Date().toISOString()});
      }

      this.http.post(endpoint, body).subscribe({
        next: () => {
          // Opcional: atualizar videoUrl ou mostrar mensagem de sucesso
        },
        error: (err) => {
          // Opcional: tratar erro
          console.error('Erro ao enviar a HotKey:', err);
        }
      });
    }
  }

    sendText(): void {
    if (this.textInput && this.keyInput) {
      const endpoint = `http://127.0.0.1:8000/text?text=${this.textInput}`;
      const body = { text: this.textInput };

      if(this.gravando){
        this.events.push({id:this.events.length, type:"text", text:this.textInput, key:this.keyInput, time:new Date().toISOString()});
      }

      this.http.post(endpoint, body).subscribe({
        next: () => {
          // Opcional: atualizar videoUrl ou mostrar mensagem de sucesso
        },
        error: (err) => {
          // Opcional: tratar erro
          console.error('Erro ao acessar a URL:', err);
        }
      });
    }
  }

  get(): void {

      const endpoint = `http://127.0.0.1:8000/getvalue`;
      const body = { text: this.textInput };

      if(this.gravando){
        this.events.push({id:this.events.length, type:"text", text:this.textInput, key:this.keyInput, time:new Date().toISOString()});
      }

      this.http.get(endpoint).subscribe({
        next: () => {
          // Opcional: atualizar videoUrl ou mostrar mensagem de sucesso
        },
        error: (err) => {
          // Opcional: tratar erro
          console.error('Erro ao acessar a URL:', err);
        }
      });
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
        this.events.push({id:this.events.length, type:"move_mouse_and_click", duration:0.0, x:this.mouseX, y:this.mouseY, event:buttonMap[event.button], time:new Date().toISOString()});
      }
    
    const url = `http://127.0.0.1:8000/move_mouse_and_click?x=${this.mouseX}&y=${this.mouseY}&duration=0&event=${buttonMap[event.button]}`;
    this.http.post(url, {}).subscribe();
  }

  onKeyDown(event: KeyboardEvent): void {
    this.lastKeyPressed = event.key;
      if(this.gravando){
        this.events.push({id:this.events.length, type:"press", key:this.lastKeyPressed, time:new Date().toISOString()});
      }
    const url = `http://127.0.0.1:8000/press?key=${this.lastKeyPressed}`;
    this.http.post(url, {}).subscribe();
  }

  onMouseWheel(event: WheelEvent) {
      if(this.gravando){
        this.events.push({id:this.events.length, type:"scroll", deltaY:event.deltaY, time:new Date().toISOString()});
      }
    const url = `http://127.0.0.1:8000/scroll?deltaY=${event.deltaY}`;
    this.http.post(url, {}).subscribe();
  }

  onGravar(): void {
    this.gravando = true;
    this.executando = false;
    this.events = [];
  }

  onParar(): void {
    this.gravando = false;
    this.executando = false;
  }

  onExecutar(): void {
    this.executando = true;
    this.gravando = false;
    const url = `http://127.0.0.1:8000/generic`;
    console.log('onExecutar', this.events);
    this.http.post(url, this.events).subscribe({
        next: () => {
          // Opcional: atualizar videoUrl ou mostrar mensagem de sucesso
        },
        error: (err) => {
          // Opcional: tratar erro
          console.error('Erro ao acessar a URL:', err);
        }
      });
    
  }

}
