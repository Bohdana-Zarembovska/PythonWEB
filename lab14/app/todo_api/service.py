from app.todo.models import Todo
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable, Tuple
from datetime import datetime

class TodoValidator:
    
    @staticmethod
    def __title_required(dto: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        if not dto.get('title'):
            return False, {
                'message': "Title must be provided",
                'status_code': 422
            }
        return True, None
    
    
    @staticmethod
    def __validate(dto: Dict[str, Any], validators: List[Callable]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        for validator in validators:
            is_valid, response = validator(dto)
            if not is_valid:
                return is_valid, response 

        return True, None

    @staticmethod
    def validate_for_create(dto: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        validators = [TodoValidator.__title_required, TodoValidator.__category_exists]
        return TodoValidator.__validate(dto, validators)

    @staticmethod
    def validate_for_update(dto: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        validators = [TodoValidator.__category_exists]
        return TodoValidator.__validate(dto, validators)


class TodoMapper:
    
    @staticmethod
    def to_dto(todo: Any) -> Dict[str, Any]:
        return {
            "id": todo.id,
            "title": todo.title, 
            "due_date": todo.due_date.strftime("%Y-%m-%d") if todo.due_date else None, 
            "complete": todo.complete,
            "category_id": todo.category_id
        }
    
    @staticmethod
    def to_entity(dto: Dict[str, Any]) -> Any:
        return Todo(
            title=dto.get('title'), 
            due_date=datetime.strptime(dto.get('due_date'), "%Y-%m-%d").date() if dto.get('due_date') else None, 
            category_id=dto.get('category_id'),
            complete=dto.get('complete', False)
        )
    
    @staticmethod
    def update_from_dto(todo: Any, dto: Dict[str, Any]) -> Any:
        title = dto.get('title')
        due_date = dto.get('due_date')
        complete = dto.get('complete')
        category_id = dto.get('category_id')

        if title:
            todo.title = title

        if due_date:
            todo.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        if complete:
            todo.complete = complete

        if category_id:
            todo.category_id = category_id

        return todo