import { Component } from '@angular/core';

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

  onMouseMove(event: MouseEvent): void {
    const rect = (event.target as HTMLImageElement).getBoundingClientRect();
    this.mouseX = Math.floor(event.clientX - rect.left);
    this.mouseY = Math.floor(event.clientY - rect.top);
  }

  onMouseDown(event: MouseEvent): void {
    const buttonMap: { [key: number]: string } = { 0: 'click-left', 1: 'click-middle', 2: 'click-right' };
    this.mouseEvent = buttonMap[event.button] || 'unknown';
  }

  onKeyDown(event: KeyboardEvent): void {
    this.lastKeyPressed = event.key;
  }
}
