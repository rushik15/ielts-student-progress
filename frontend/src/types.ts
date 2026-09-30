export type Role = 'student'|'teacher'|'admin'; export type Skill = 'listening'|'reading'|'writing';
export interface User {id:number; student_number:string; full_name:string; email?:string|null; role:Role; is_active:boolean}
export interface Mistake {id?:number; category?:string|null; question_reference?:string|null; description:string; correction?:string|null}
export interface Score {id:number; student_id:number; skill:Skill; writing_task?:number|null; test_name:string; test_date:string; band_score:number; raw_score?:number|null; total_questions?:number|null; mistake_summary?:string|null; teacher_note?:string|null; mistakes:Mistake[]}
export interface Progress {skill:Skill; latest:number|null; best:number|null; average:number|null; count:number; points:{id:number;test_name:string;test_date:string;band_score:number}[]}
