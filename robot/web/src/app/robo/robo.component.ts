import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-robo',
  templateUrl: './robo.component.html',
  styleUrls: ['./robo.component.css']
})
export class RoboComponent {
  videoUrl: string = 'http://localhost:5000/video';
  mouseX: number = 0;
  mouseY: number = 0;
  mouseEvent: string = '';
  lastKeyPressed: string = '';

  constructor(private http: HttpClient) {}

  onMouseMove(event: MouseEvent): void {
    const rect = (event.target as HTMLImageElement).getBoundingClientRect();
    this.mouseX = Math.floor(event.clientX - rect.left);
    this.mouseY = Math.floor(event.clientY - rect.top);
  }

  onMouseDown(event: MouseEvent): void {
    const buttonMap: { [key: number]: string } = { 0: 'left', 1: 'middle', 2: 'right' };
    this.mouseEvent = buttonMap[event.button] || 'unknown';
    
    const url = `http://127.0.0.1:8000/move_mouse_and_click?x=${this.mouseX}&y=${this.mouseY}&duration=0&event=${buttonMap[event.button]}`;
    this.http.post(url, {}).subscribe();
  }

  onKeyDown(event: KeyboardEvent): void {
    this.lastKeyPressed = event.key;
  }


}
