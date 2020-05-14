from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from user.permissions import CustomerPremission
from user.models import Users
from workorder.models.workorderbase import WorkOrderBase
import datetime

class ShowChartsViewSet(APIView):
    
    # 权限相关
    permission_classes = [CustomerPremission,]
    module_perms = ['charts:showcharts']
    def get(self,request,format=None):
        results = {}
        # 获取用户总数
        user_total = Users.objects.all().count()
        results['user_total'] = user_total
        # 获取工单总数
        workorder_total = WorkOrderBase.objects.all().count()
        results['workorder_total'] = workorder_total
        # 获取待处理工单
        todo_workorder = WorkOrderBase.objects.filter(~Q(status__in=[-1,1,2])).count()
        results['todo_workorder'] = todo_workorder
        # 获取已处理工单
        done_workorder = WorkOrderBase.objects.filter(Q(status__in=[1,2])).count()
        results['done_workorder'] = done_workorder
        # 获取异常工单
        exception_workorder = WorkOrderBase.objects.filter(Q(status__in=[-1])).count()
        results['exception_workorder'] = exception_workorder
        # 获取今日工单数
        today_workorder = WorkOrderBase.objects.filter(Q(create_time__contains=datetime.date.today())).count()
        results['today_workorder'] = today_workorder
        # 获取最近7天时间列表
        laste_data = []
        for i in range(6,-1,-1):
            laste_data.append(datetime.date.today() - datetime.timedelta(days=i))
        results['laste_data'] = laste_data
        # 获取最近7天每种工单的数量
        laste_sql = []
        laste_auto = []
        laste_ops = []
        for i in laste_data:
            # 获取最近7天需求工单每天总数
            laste_ops_count = WorkOrderBase.objects.filter(Q(classify='OpsOnline'),Q(create_time__contains=i)).count()
            laste_ops.append(laste_ops_count)
            results['laste_ops'] = laste_ops
            # 获取最近7天自助工单每天总数
            laste_auto_count = WorkOrderBase.objects.filter(Q(classify='AutoOnline'),Q(create_time__contains=i)).count()
            laste_auto.append(laste_auto_count)
            results['laste_auto'] = laste_auto
        # 获取每种工单历史总量
        # ops工单历史总量
        hisops_total = WorkOrderBase.objects.filter(Q(classify='OpsOnline')).count()
        results['hisops_total'] = hisops_total
        # auto工单历史总量
        hisauto_total = WorkOrderBase.objects.filter(Q(classify='AutoOnline')).count()
        results['hisauto_total'] = hisauto_total

        re = { 'results': '',}
        re['results'] = results
        return Response(re)
