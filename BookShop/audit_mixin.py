import logging

audit_logger = logging.getLogger('audit_logger')


class AuditLogMixin:
    def _is_admin(self) -> bool:
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.is_superuser)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if self._is_admin():
            instance = serializer.instance
            audit_logger.info(
                'CREATE | admin=%s | model=%s | pk=%s | data=%s',
                self.request.user.id,
                type(instance).__name__,
                instance.pk,
                serializer.validated_data,
            )

    def perform_update(self, serializer):
        is_admin = self._is_admin()
        if is_admin:
            instance = serializer.instance
            model_name = type(instance).__name__
            before = {k: getattr(instance, k, None) for k in serializer.validated_data}
        super().perform_update(serializer)
        if is_admin:
            changes = {
                k: {'before': str(before[k]), 'after': str(serializer.validated_data[k])}
                for k in before
                if str(before[k]) != str(serializer.validated_data[k])
            }
            audit_logger.info(
                'UPDATE | admin=%s | model=%s | pk=%s | changes=%s',
                self.request.user.id,
                model_name,
                serializer.instance.pk,
                changes,
            )

    def perform_destroy(self, instance):
        is_admin = self._is_admin()
        if is_admin:
            model_name = type(instance).__name__
            pk = instance.pk
        super().perform_destroy(instance)
        if is_admin:
            audit_logger.info(
                'DELETE | admin=%s | model=%s | pk=%s',
                self.request.user.id,
                model_name,
                pk,
            )
