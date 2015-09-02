task :default => :test

task :test => ["test:unit", "test:integration"]

namespace :test do
  desc "run unit tests"
  task :unit do
    sh "nosetests tests/unit"
  end

  desc "run integration tests"
  task :integration do
    sh "env nosetests tests/integration"
  end

  desc "run single test (example: rake test:single[tests/integration/test_paypal_account.py:TestPayPalAccount.test_find_returns_paypal_account])"
  task :single, [:test_name] do |t, args|
      sh "nosetests #{args[:test_name]}"
  end
end

task :clean do
  rm_rf "build"
  rm_rf "dist"
  rm_f "MANIFEST"
end

namespace :pypi do
  desc "Register the package with PyPI"
  task :register => :clean do
    sh "python setup.py register"
  end

  desc "Upload a new version to PyPI"
  task :upload => :clean do
    sh "python setup.py sdist upload"
  end
end
