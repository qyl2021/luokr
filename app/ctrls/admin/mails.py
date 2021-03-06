# -*- coding: UTF-8 -*-

from . import admin, AdminCtrl

class Admin_MailsCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        mails = self.datum('mails').result(
                'select * from mails order by mail_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        if mails:
            pager['lgth'] = len(mails)

        self.render('admin/mails.html', pager = pager, mails = mails)

class Admin_MailAccessCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            mail_id = self.input('mail_id')

            if self.datum('mails').submit(
                    'update mails set mail_stat=1, mail_utms=? where mail_id = ?', (self.stime(), mail_id,)).rowcount:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_MailResendCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            mail = self.datum('mails').record('select * from mails where mail_id = ?', (self.input('mail_id'),))
            if not mail:
                self.flash(0)
                return

            self.flash(1)
            self.email('%s <%s>' %(mail['user_name'], mail['user_mail']), self.jsons(self.get_runtime_conf('mails')),
                    'Received Feedback (%s)' % self.timer().strftime('%F %T %Z', self.timer().localtime(mail['mail_ctms'])),
                    'Mail From %s <%s>:\r\n\r\n%s' %(mail['user_name'], mail['user_mail'], mail['mail_text']))
            return
        except:
            pass
        self.flash(0)

class Admin_MailDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            mail_id   = self.input('mail_id')
            mail_utms = self.input('mail_utms')

            if self.datum('mails').submit(
                    'delete from mails where mail_id = ? and mail_utms = ?', (mail_id, mail_utms ,)).rowcount:
                self.ualog(self.current_user, '???????????????' + str(mail_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
